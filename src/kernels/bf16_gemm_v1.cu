#include "kernel_api.h"

#include <cuda_bf16.h>
#include <cuda_runtime.h>
#include <mma.h>

namespace matmul_optimizer {
namespace {

namespace wmma = nvcuda::wmma;

constexpr int kFallbackTileM = 16;
constexpr int kFallbackTileN = 16;
constexpr int kFallbackTileK = 16;

constexpr int kWmmaM = 16;
constexpr int kWmmaN = 16;
constexpr int kWmmaK = 16;
constexpr int kWarpSize = 32;
constexpr int kWarpTilesM = 2;
// Expand the CTA to a 2x2 warp layout so each staged K-slice feeds four warps
// instead of two while preserving the existing per-warp MMA shape.
constexpr int kWarpTilesN = 2;
// Each warp still spans three adjacent 16x16 output tiles along N so it can
// reuse the same A fragment across more MMA work per shared-memory feed.
constexpr int kWarpMmaTilesN = 3;
constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
constexpr int kTensorBlockM = kWarpTilesM * kWmmaM;
constexpr int kTensorBlockN = kWarpTilesN * kWarpMmaTilesN * kWmmaN;
constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
// Reuse a single 16x16 scratch tile per warp during the epilogue instead of
// materializing all N tiles in shared memory at once.
constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
constexpr int kAsyncCopyElems = 8;
constexpr int kAsyncCopyBytes = kAsyncCopyElems * sizeof(__nv_bfloat16);
constexpr int kWarpGroupCols = kWarpMmaTilesN * kWmmaN;
// Keep the B tile row-major for WMMA, but route the single 16-byte skew
// between the two 48-column warp groups so each warp reads a more local slice
// without increasing the accepted 16x104 shared-memory footprint.
constexpr int kBSharedStride = kTensorBlockN + kAsyncCopyElems;
constexpr int kBSharedTileElems = kWmmaK * kBSharedStride;
constexpr int kBStagedTileElems = kWmmaK * kTensorBlockN;
constexpr int kAAsyncCopiesPerRow = kWmmaK / kAsyncCopyElems;
constexpr int kBAsyncCopiesPerRow = kTensorBlockN / kAsyncCopyElems;
constexpr int kAAsyncCopiesPerTile = kASharedTileElems / kAsyncCopyElems;
constexpr int kBAsyncCopiesPerTile = kBStagedTileElems / kAsyncCopyElems;

static_assert(kAsyncCopyBytes == 16, "Tensor-core staging expects 16-byte async copies.");
static_assert((kWmmaK % kAsyncCopyElems) == 0, "A tile width must stay 16-byte aligned.");
static_assert((kTensorBlockN % kAsyncCopyElems) == 0, "B tile width must stay 16-byte aligned.");
static_assert((kWarpGroupCols % kAsyncCopyElems) == 0, "Each warp-group span must stay 16-byte aligned.");
static_assert((kBSharedStride % kAsyncCopyElems) == 0, "B shared stride must stay 16-byte aligned.");
static_assert((kASharedTileElems % kAsyncCopyElems) == 0, "A tile must be divisible by async copy width.");
static_assert((kBSharedTileElems % kAsyncCopyElems) == 0, "B tile must be divisible by async copy width.");

__device__ __forceinline__ void cp_async_copy_16_bytes(
    __nv_bfloat16* dst,
    const __nv_bfloat16* src) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  const unsigned int dst_addr =
      static_cast<unsigned int>(__cvta_generic_to_shared(dst));
  asm volatile("cp.async.ca.shared.global [%0], [%1], %2;\n" :: "r"(dst_addr), "l"(src), "n"(kAsyncCopyBytes));
#else
  (void)dst;
  (void)src;
#endif
}

__device__ __forceinline__ void cp_async_commit_group() {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  asm volatile("cp.async.commit_group;\n" ::);
#endif
}

__device__ __forceinline__ void cp_async_wait_group_0() {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  asm volatile("cp.async.wait_group 0;\n" ::);
#endif
}

__host__ __device__ __forceinline__ int b_shared_col_from_logical(int logical_col) {
  return logical_col + (logical_col / kWarpGroupCols) * kAsyncCopyElems;
}

__device__ __forceinline__ void stage_a_shared_tile_async(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  for (int copy_idx = threadIdx.x; copy_idx < kAAsyncCopiesPerTile; copy_idx += blockDim.x) {
    const int row = copy_idx / kAAsyncCopiesPerRow;
    const int col = (copy_idx % kAAsyncCopiesPerRow) * kAsyncCopyElems;
    cp_async_copy_16_bytes(
        shared_tile + row * kWmmaK + col,
        global_tile + row * global_stride + col);
  }
}

__device__ __forceinline__ void stage_b_shared_tile_async(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  for (int copy_idx = threadIdx.x; copy_idx < kBAsyncCopiesPerTile; copy_idx += blockDim.x) {
    const int row = copy_idx / kBAsyncCopiesPerRow;
    const int logical_col = (copy_idx % kBAsyncCopiesPerRow) * kAsyncCopyElems;
    const int shared_col = b_shared_col_from_logical(logical_col);
    cp_async_copy_16_bytes(
        shared_tile + row * kBSharedStride + shared_col,
        global_tile + row * global_stride + logical_col);
  }
}

__host__ __device__ __forceinline__ int ceil_div(int value, int divisor) {
  return (value + divisor - 1) / divisor;
}

__global__ void bf16_gemm_v1_fallback_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k) {
  __shared__ float a_tile[kFallbackTileM][kFallbackTileK];
  __shared__ float b_tile[kFallbackTileK][kFallbackTileN];

  const int row = blockIdx.y * kFallbackTileM + threadIdx.y;
  const int col = blockIdx.x * kFallbackTileN + threadIdx.x;

  float acc = 0.0f;

  for (int tile_k = 0; tile_k < k; tile_k += kFallbackTileK) {
    const int a_col = tile_k + threadIdx.x;
    const int b_row = tile_k + threadIdx.y;

    a_tile[threadIdx.y][threadIdx.x] =
        (row < m && a_col < k) ? __bfloat162float(a[row * k + a_col]) : 0.0f;
    b_tile[threadIdx.y][threadIdx.x] =
        (b_row < k && col < n) ? __bfloat162float(b[b_row * n + col]) : 0.0f;

    __syncthreads();

    #pragma unroll
    for (int kk = 0; kk < kFallbackTileK; ++kk) {
      acc += a_tile[threadIdx.y][kk] * b_tile[kk][threadIdx.x];
    }

    __syncthreads();
  }

  if (row < m && col < n) {
    c[row * n + col] = __float2bfloat16(acc);
  }
}

__global__ void bf16_gemm_v1_tensor_core_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  __shared__ __align__(16) __nv_bfloat16 a_shared[2][kASharedTileElems];
  __shared__ __align__(16) __nv_bfloat16 b_shared[2][kBSharedTileElems];
  __shared__ __align__(16) float c_shared[kWarpsPerBlock * kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= kWarpsPerBlock) {
    return;
  }

  const int block_row = blockIdx.y * kTensorBlockM;
  const int block_col = blockIdx.x * kTensorBlockN;
  const int warp_tile_m = warp_id / kWarpTilesN;
  const int warp_tile_n = warp_id % kWarpTilesN;
  const int row = block_row + warp_tile_m * kWmmaM;
  const int col = block_col + warp_tile_n * kWarpMmaTilesN * kWmmaN;

  wmma::fragment<wmma::accumulator, kWmmaM, kWmmaN, kWmmaK, float> acc_frags[kWarpMmaTilesN];
  #pragma unroll
  for (int tile_n = 0; tile_n < kWarpMmaTilesN; ++tile_n) {
    wmma::fill_fragment(acc_frags[tile_n], 0.0f);
  }

  const __nv_bfloat16* a_tile_0 = a + block_row * k;
  const __nv_bfloat16* b_tile_0 = b + block_col;

  stage_a_shared_tile_async(a_shared[0], a_tile_0, k);
  stage_b_shared_tile_async(b_shared[0], b_tile_0, n);
  cp_async_commit_group();
  cp_async_wait_group_0();
  __syncthreads();

  for (int tile_k = 0; tile_k < k; tile_k += kWmmaK) {
    const int next_tile_k = tile_k + kWmmaK;
    const int curr_stage = (tile_k / kWmmaK) & 1;
    const int next_stage = curr_stage ^ 1;

    wmma::fragment<wmma::matrix_a, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> a_frag;
    wmma::fragment<wmma::matrix_b, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> b_frags[kWarpMmaTilesN];

    if (next_tile_k < k) {
      const __nv_bfloat16* a_next_tile = a + block_row * k + next_tile_k;
      const __nv_bfloat16* b_next_tile = b + next_tile_k * n + block_col;
      stage_a_shared_tile_async(a_shared[next_stage], a_next_tile, k);
      stage_b_shared_tile_async(b_shared[next_stage], b_next_tile, n);
      cp_async_commit_group();
    }

    const __nv_bfloat16* a_tile = a_shared[curr_stage] + warp_tile_m * kWmmaM * kWmmaK;
    const __nv_bfloat16* b_tile =
        b_shared[curr_stage] + b_shared_col_from_logical(warp_tile_n * kWarpGroupCols);

    wmma::load_matrix_sync(a_frag, a_tile, kWmmaK);
    #pragma unroll
    for (int tile_n = 0; tile_n < kWarpMmaTilesN; ++tile_n) {
      wmma::load_matrix_sync(b_frags[tile_n], b_tile + tile_n * kWmmaN, kBSharedStride);
      wmma::mma_sync(acc_frags[tile_n], a_frag, b_frags[tile_n], acc_frags[tile_n]);
    }

    if (next_tile_k < k) {
      cp_async_wait_group_0();
      __syncthreads();
    }
  }

  float* warp_c_tile = c_shared + warp_id * kCSharedTileElemsPerWarp;
  #pragma unroll
  for (int tile_n = 0; tile_n < kWarpMmaTilesN; ++tile_n) {
    wmma::store_matrix_sync(
        warp_c_tile,
        acc_frags[tile_n],
        kWmmaN,
        wmma::mem_row_major);
    __syncwarp();

    #pragma unroll
    for (int tile_elem = lane_id; tile_elem < kCSharedTileElemsPerWarp; tile_elem += kWarpSize) {
      const int local_row = tile_elem / kWmmaN;
      const int local_col = tile_elem % kWmmaN;
      c[(row + local_row) * n + col + tile_n * kWmmaN + local_col] =
          __float2bfloat16(warp_c_tile[tile_elem]);
    }
    __syncwarp();
  }
#else
  (void)a;
  (void)b;
  (void)c;
  (void)m;
  (void)n;
  (void)k;
#endif
}

}  // namespace

bool launch_bf16_gemm_v1(
    const std::uint16_t* a_bf16,
    const std::uint16_t* b_bf16,
    std::uint16_t* c_bf16,
    int m,
    int n,
    int k,
    cudaStream_t stream) {
  if (a_bf16 == nullptr || b_bf16 == nullptr || c_bf16 == nullptr) {
    return false;
  }
  if (m <= 0 || n <= 0 || k <= 0) {
    return false;
  }

  const auto* a = reinterpret_cast<const __nv_bfloat16*>(a_bf16);
  const auto* b = reinterpret_cast<const __nv_bfloat16*>(b_bf16);
  auto* c = reinterpret_cast<__nv_bfloat16*>(c_bf16);

  if ((m % kTensorBlockM) == 0 && (n % kTensorBlockN) == 0 && (k % kWmmaK) == 0) {
    const dim3 block(kWarpsPerBlock * kWarpSize, 1, 1);
    const dim3 grid(ceil_div(n, kTensorBlockN), ceil_div(m, kTensorBlockM), 1);
    bf16_gemm_v1_tensor_core_kernel<<<grid, block, 0, stream>>>(a, b, c, m, n, k);
  } else {
    const dim3 block(kFallbackTileN, kFallbackTileM, 1);
    const dim3 grid(ceil_div(n, kFallbackTileN), ceil_div(m, kFallbackTileM), 1);
    bf16_gemm_v1_fallback_kernel<<<grid, block, 0, stream>>>(a, b, c, m, n, k);
  }

  return cudaGetLastError() == cudaSuccess;
}

}  // namespace matmul_optimizer
