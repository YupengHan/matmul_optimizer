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
constexpr int kEpilogueVecElems = 2;
constexpr int kAsyncCopyElems = 8;
constexpr int kAsyncCopyBytes = kAsyncCopyElems * sizeof(__nv_bfloat16);

template <int WarpTilesMValue, int WarpTilesNValue, int WarpMmaTilesNValue>
struct TensorCoreTileConfig {
  static constexpr int kWarpTilesM = WarpTilesMValue;
  static constexpr int kWarpTilesN = WarpTilesNValue;
  static constexpr int kWarpMmaTilesN = WarpMmaTilesNValue;
  static constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
  static constexpr int kTensorBlockM = kWarpTilesM * kWmmaM;
  static constexpr int kTensorBlockN = kWarpTilesN * kWarpMmaTilesN * kWmmaN;
  static constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
  // Reuse a single 16x16 scratch tile per warp during the epilogue instead of
  // materializing all N tiles in shared memory at once.
  static constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
  static constexpr int kWarpGroupCols = kWarpMmaTilesN * kWmmaN;
  // Keep the B tile row-major for WMMA, but place one 16-byte skew between
  // adjacent warp groups so each group keeps a local slice without overlap.
  static constexpr int kBSharedSkewGaps = kWarpTilesN - 1;
  static constexpr int kBSharedStride = kTensorBlockN + kBSharedSkewGaps * kAsyncCopyElems;
  static constexpr int kBSharedTileElems = kWmmaK * kBSharedStride;
  static constexpr int kBStagedTileElems = kWmmaK * kTensorBlockN;
  static constexpr int kAAsyncCopiesPerRow = kWmmaK / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerRow = kTensorBlockN / kAsyncCopyElems;
  static constexpr int kAAsyncCopiesPerTile = kASharedTileElems / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerTile = kBStagedTileElems / kAsyncCopyElems;
};

// Keep the accepted 64x96 tail specialization intact while retiling the hot
// 128-wide main path to a 2x4 warp layout with fewer N fragments per warp.
using TensorCoreTile96 = TensorCoreTileConfig<4, 2, 3>;
using TensorCoreTile128 = TensorCoreTileConfig<2, 4, 2>;

constexpr int kFixedBenchmarkM = 6464;
constexpr int kFixedBenchmarkN = 7776;
constexpr int kFixedBenchmarkK = 7232;
constexpr int kFixedTailRegionN = TensorCoreTile96::kTensorBlockN;
constexpr int kFixedMainRegionN = kFixedBenchmarkN - kFixedTailRegionN;

static_assert(kAsyncCopyBytes == 16, "Tensor-core staging expects 16-byte async copies.");
static_assert(TensorCoreTile96::kWarpTilesM == 4 && TensorCoreTile96::kWarpTilesN == 2, "Tail path keeps the established 4x2 warp layout.");
static_assert(TensorCoreTile96::kTensorBlockM == 64, "Tail path expects a fixed 64x96 CTA tile.");
static_assert(TensorCoreTile96::kTensorBlockN == 96, "Tail path expects a fixed 64x96 CTA tile.");
static_assert(TensorCoreTile96::kWarpsPerBlock == 8, "Tail path expects an 8-warp CTA.");
static_assert(TensorCoreTile128::kWarpTilesM == 2 && TensorCoreTile128::kWarpTilesN == 4, "Main path expects the retiled 2x4 warp layout.");
static_assert(TensorCoreTile128::kTensorBlockM == 32, "Main path expects a fixed 32x128 CTA tile.");
static_assert(TensorCoreTile128::kTensorBlockN == 128, "Main path expects a fixed 32x128 CTA tile.");
static_assert(TensorCoreTile128::kWarpsPerBlock == 8, "Main path expects an 8-warp CTA.");
static_assert((kWmmaK % kAsyncCopyElems) == 0, "A tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kTensorBlockN % kAsyncCopyElems) == 0, "Tail B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kWarpGroupCols % kAsyncCopyElems) == 0, "Tail warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kBSharedStride % kAsyncCopyElems) == 0, "Tail B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kASharedTileElems % kAsyncCopyElems) == 0, "A tile must be divisible by async copy width.");
static_assert((TensorCoreTile96::kBSharedTileElems % kAsyncCopyElems) == 0, "Tail B tile must be divisible by async copy width.");
static_assert((TensorCoreTile128::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((kFixedBenchmarkM % TensorCoreTile96::kTensorBlockM) == 0, "Fixed benchmark rows must fit the 64x96 tail CTA height.");
static_assert((kFixedBenchmarkM % TensorCoreTile128::kTensorBlockM) == 0, "Fixed benchmark rows must fit the 32x128 main CTA height.");
static_assert((kFixedMainRegionN % TensorCoreTile128::kTensorBlockN) == 0, "Fixed-shape main region must be an even count of 32x128 CTAs.");
static_assert(kFixedMainRegionN + kFixedTailRegionN == kFixedBenchmarkN, "Main/tail split must cover the fixed benchmark width exactly.");
static_assert((kWmmaN % kEpilogueVecElems) == 0, "Epilogue vector stores require adjacent column pairs.");

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

__device__ __forceinline__ void store_bfloat162_pair(
    __nv_bfloat16* dst,
    const float2 values) {
  *reinterpret_cast<__nv_bfloat162*>(dst) = __float22bfloat162_rn(values);
}

template <typename TileConfig>
__host__ __device__ __forceinline__ int b_shared_col_from_logical(int logical_col) {
  return logical_col + (logical_col / TileConfig::kWarpGroupCols) * kAsyncCopyElems;
}

template <typename TileConfig>
__device__ __forceinline__ void stage_a_shared_tile_async(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  for (int copy_idx = threadIdx.x; copy_idx < TileConfig::kAAsyncCopiesPerTile; copy_idx += blockDim.x) {
    const int row = copy_idx / TileConfig::kAAsyncCopiesPerRow;
    const int col = (copy_idx % TileConfig::kAAsyncCopiesPerRow) * kAsyncCopyElems;
    cp_async_copy_16_bytes(
        shared_tile + row * kWmmaK + col,
        global_tile + row * global_stride + col);
  }
}

template <typename TileConfig>
__device__ __forceinline__ void stage_b_shared_tile_async(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  for (int copy_idx = threadIdx.x; copy_idx < TileConfig::kBAsyncCopiesPerTile; copy_idx += blockDim.x) {
    const int row = copy_idx / TileConfig::kBAsyncCopiesPerRow;
    const int logical_col = (copy_idx % TileConfig::kBAsyncCopiesPerRow) * kAsyncCopyElems;
    const int shared_col = b_shared_col_from_logical<TileConfig>(logical_col);
    cp_async_copy_16_bytes(
        shared_tile + row * TileConfig::kBSharedStride + shared_col,
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

template <typename TileConfig>
__global__ void bf16_gemm_v1_tensor_core_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  __shared__ __align__(16) __nv_bfloat16 a_shared[2][TileConfig::kASharedTileElems];
  __shared__ __align__(16) __nv_bfloat16 b_shared[2][TileConfig::kBSharedTileElems];
  __shared__ __align__(16) float c_shared[TileConfig::kWarpsPerBlock * TileConfig::kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= TileConfig::kWarpsPerBlock) {
    return;
  }

  const int block_row = blockIdx.y * TileConfig::kTensorBlockM;
  const int block_col = blockIdx.x * TileConfig::kTensorBlockN;
  const int warp_tile_m = warp_id / TileConfig::kWarpTilesN;
  const int warp_tile_n = warp_id % TileConfig::kWarpTilesN;
  const int row = block_row + warp_tile_m * kWmmaM;
  const int col = block_col + warp_tile_n * TileConfig::kWarpMmaTilesN * kWmmaN;

  wmma::fragment<wmma::accumulator, kWmmaM, kWmmaN, kWmmaK, float> acc_frags[TileConfig::kWarpMmaTilesN];
  #pragma unroll
  for (int tile_n = 0; tile_n < TileConfig::kWarpMmaTilesN; ++tile_n) {
    wmma::fill_fragment(acc_frags[tile_n], 0.0f);
  }

  const __nv_bfloat16* a_tile_0 = a + block_row * k;
  const __nv_bfloat16* b_tile_0 = b + block_col;

  stage_a_shared_tile_async<TileConfig>(a_shared[0], a_tile_0, k);
  stage_b_shared_tile_async<TileConfig>(b_shared[0], b_tile_0, n);
  cp_async_commit_group();
  cp_async_wait_group_0();
  __syncthreads();

  for (int tile_k = 0; tile_k < k; tile_k += kWmmaK) {
    const int next_tile_k = tile_k + kWmmaK;
    const int curr_stage = (tile_k / kWmmaK) & 1;
    const int next_stage = curr_stage ^ 1;

    wmma::fragment<wmma::matrix_a, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> a_frag;
    wmma::fragment<wmma::matrix_b, kWmmaM, kWmmaN, kWmmaK, __nv_bfloat16, wmma::row_major> b_frags[TileConfig::kWarpMmaTilesN];

    if (next_tile_k < k) {
      const __nv_bfloat16* a_next_tile = a + block_row * k + next_tile_k;
      const __nv_bfloat16* b_next_tile = b + next_tile_k * n + block_col;
      stage_a_shared_tile_async<TileConfig>(a_shared[next_stage], a_next_tile, k);
      stage_b_shared_tile_async<TileConfig>(b_shared[next_stage], b_next_tile, n);
      cp_async_commit_group();
    }

    const __nv_bfloat16* a_tile = a_shared[curr_stage] + warp_tile_m * kWmmaM * kWmmaK;
    const __nv_bfloat16* b_tile =
        b_shared[curr_stage] + b_shared_col_from_logical<TileConfig>(warp_tile_n * TileConfig::kWarpGroupCols);

    wmma::load_matrix_sync(a_frag, a_tile, kWmmaK);
    #pragma unroll
    for (int tile_n = 0; tile_n < TileConfig::kWarpMmaTilesN; ++tile_n) {
      wmma::load_matrix_sync(b_frags[tile_n], b_tile + tile_n * kWmmaN, TileConfig::kBSharedStride);
      wmma::mma_sync(acc_frags[tile_n], a_frag, b_frags[tile_n], acc_frags[tile_n]);
    }

    if (next_tile_k < k) {
      cp_async_wait_group_0();
      __syncthreads();
    }
  }

  float* warp_c_tile = c_shared + warp_id * TileConfig::kCSharedTileElemsPerWarp;
  #pragma unroll
  for (int tile_n = 0; tile_n < TileConfig::kWarpMmaTilesN; ++tile_n) {
    wmma::store_matrix_sync(
        warp_c_tile,
        acc_frags[tile_n],
        kWmmaN,
        wmma::mem_row_major);
    __syncwarp();

    const float2* warp_c_tile_pairs = reinterpret_cast<const float2*>(warp_c_tile);
    constexpr int kPairsPerRow = kWmmaN / kEpilogueVecElems;
    constexpr int kPairsPerTile = TileConfig::kCSharedTileElemsPerWarp / kEpilogueVecElems;

    #pragma unroll
    for (int pair_idx = lane_id; pair_idx < kPairsPerTile; pair_idx += kWarpSize) {
      const int local_row = pair_idx / kPairsPerRow;
      const int local_col = (pair_idx % kPairsPerRow) * kEpilogueVecElems;
      store_bfloat162_pair(
          c + (row + local_row) * n + col + tile_n * kWmmaN + local_col,
          warp_c_tile_pairs[pair_idx]);
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

  if (m == kFixedBenchmarkM && n == kFixedBenchmarkN && k == kFixedBenchmarkK) {
    const dim3 main_block(TensorCoreTile128::kWarpsPerBlock * kWarpSize, 1, 1);
    const dim3 main_grid(kFixedMainRegionN / TensorCoreTile128::kTensorBlockN, m / TensorCoreTile128::kTensorBlockM, 1);
    bf16_gemm_v1_tensor_core_kernel<TensorCoreTile128><<<main_grid, main_block, 0, stream>>>(a, b, c, m, n, k);

    const dim3 tail_block(TensorCoreTile96::kWarpsPerBlock * kWarpSize, 1, 1);
    const dim3 tail_grid(kFixedTailRegionN / TensorCoreTile96::kTensorBlockN, m / TensorCoreTile96::kTensorBlockM, 1);
    bf16_gemm_v1_tensor_core_kernel<TensorCoreTile96><<<tail_grid, tail_block, 0, stream>>>(
        a,
        b + kFixedMainRegionN,
        c + kFixedMainRegionN,
        m,
        n,
        k);
  } else if ((m % TensorCoreTile96::kTensorBlockM) == 0 &&
             (n % TensorCoreTile96::kTensorBlockN) == 0 &&
             (k % kWmmaK) == 0) {
    const dim3 block(TensorCoreTile96::kWarpsPerBlock * kWarpSize, 1, 1);
    const dim3 grid(ceil_div(n, TensorCoreTile96::kTensorBlockN), ceil_div(m, TensorCoreTile96::kTensorBlockM), 1);
    bf16_gemm_v1_tensor_core_kernel<TensorCoreTile96><<<grid, block, 0, stream>>>(a, b, c, m, n, k);
  } else {
    const dim3 block(kFallbackTileN, kFallbackTileM, 1);
    const dim3 grid(ceil_div(n, kFallbackTileN), ceil_div(m, kFallbackTileM), 1);
    bf16_gemm_v1_fallback_kernel<<<grid, block, 0, stream>>>(a, b, c, m, n, k);
  }

  return cudaGetLastError() == cudaSuccess;
}

}  // namespace matmul_optimizer
