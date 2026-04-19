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
constexpr int kWarpTilesN = 2;
constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
constexpr int kTensorBlockM = kWarpTilesM * kWmmaM;
constexpr int kTensorBlockN = kWarpTilesN * kWmmaN;
constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
constexpr int kBSharedTileElems = kWmmaK * kTensorBlockN;
constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
constexpr int kAsyncCopyElems = 4;
constexpr int kAsyncCopyBytes = kAsyncCopyElems * sizeof(__nv_bfloat16);

__device__ __forceinline__ void cp_async_copy_8_bytes(
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

__device__ __forceinline__ void stage_shared_tile_async(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride,
    int tile_cols,
    int total_elems) {
  for (int chunk = threadIdx.x; chunk < total_elems / kAsyncCopyElems; chunk += blockDim.x) {
    const int elem = chunk * kAsyncCopyElems;
    const int row = elem / tile_cols;
    const int col = elem % tile_cols;
    cp_async_copy_8_bytes(shared_tile + elem, global_tile + row * global_stride + col);
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
  const int col = block_col + warp_tile_n * kWmmaN;

  wmma::fragment<wmma::accumulator, kWmmaM, kWmmaN, kWmmaK, float> acc_frag;
  wmma::fill_fragment(acc_frag, 0.0f);

  const __nv_bfloat16* a_tile_0 = a + block_row * k;
  const __nv_bfloat16* b_tile_0 = b + block_col;

  stage_shared_tile_async(a_shared[0], a_tile_0, k, kWmmaK, kASharedTileElems);
  stage_shared_tile_async(b_shared[0], b_tile_0, n, kTensorBlockN, kBSharedTileElems);
  cp_async_commit_group();
  cp_async_wait_group_0();
  __syncthreads();

  for (int tile_k = 0; tile_k < k; tile_k += kWmmaK) {
    const int next_tile_k = tile_k + kWmmaK;
    const int curr_stage = (tile_k / kWmmaK) & 1;
    const int next_stage = curr_stage ^ 1;

    wmma::fragment<wmma::matrix_a, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> a_frag;
    wmma::fragment<wmma::matrix_b, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> b_frag;

    if (next_tile_k < k) {
      const __nv_bfloat16* a_next_tile = a + block_row * k + next_tile_k;
      const __nv_bfloat16* b_next_tile = b + next_tile_k * n + block_col;
      stage_shared_tile_async(a_shared[next_stage], a_next_tile, k, kWmmaK, kASharedTileElems);
      stage_shared_tile_async(b_shared[next_stage], b_next_tile, n, kTensorBlockN, kBSharedTileElems);
      cp_async_commit_group();
    }

    const __nv_bfloat16* a_tile = a_shared[curr_stage] + warp_tile_m * kWmmaM * kWmmaK;
    const __nv_bfloat16* b_tile = b_shared[curr_stage] + warp_tile_n * kWmmaN;

    wmma::load_matrix_sync(a_frag, a_tile, kWmmaK);
    wmma::load_matrix_sync(b_frag, b_tile, kTensorBlockN);
    wmma::mma_sync(acc_frag, a_frag, b_frag, acc_frag);

    if (next_tile_k < k) {
      cp_async_wait_group_0();
      __syncthreads();
    }
  }

  float* warp_c_tile = c_shared + warp_id * kCSharedTileElemsPerWarp;
  wmma::store_matrix_sync(warp_c_tile, acc_frag, kWmmaN, wmma::mem_row_major);
  __syncwarp();

  #pragma unroll
  for (int idx = lane_id; idx < kCSharedTileElemsPerWarp; idx += kWarpSize) {
    const int local_row = idx / kWmmaN;
    const int local_col = idx % kWmmaN;
    c[(row + local_row) * n + col + local_col] = __float2bfloat16(warp_c_tile[idx]);
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
