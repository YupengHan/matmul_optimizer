#include "kernel_api.h"

#include <cstdio>
#include <cstdlib>
#include <limits>

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
// Expand the CTA along M to a fixed 4x2 warp layout so each staged K-slice
// feeds eight warps while preserving the round-7 N-side organization.
constexpr int kTensorWarpTilesM = 4;
constexpr int kTensorWarpTilesN = 2;
constexpr int kAsyncCopyElems = 8;
constexpr int kAsyncCopyBytes = kAsyncCopyElems * sizeof(__nv_bfloat16);

template <int WarpMmaTilesNValue>
struct TensorCoreTileConfig {
  static constexpr int kWarpTilesM = kTensorWarpTilesM;
  static constexpr int kWarpTilesN = kTensorWarpTilesN;
  static constexpr int kWarpMmaTilesN = WarpMmaTilesNValue;
  static constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
  static constexpr int kTensorBlockM = kWarpTilesM * kWmmaM;
  static constexpr int kTensorBlockN = kWarpTilesN * kWarpMmaTilesN * kWmmaN;
  static constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
  // Reuse a single 16x16 scratch tile per warp during the epilogue instead of
  // materializing all N tiles in shared memory at once.
  static constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
  static constexpr int kWarpGroupCols = kWarpMmaTilesN * kWmmaN;
  // Keep the validated 64x384 macro tile, but repack its hot B feed path into
  // per-fragment shared tiles so WMMA loads no longer walk a wide 392-element
  // row stride. Other tile shapes keep the existing row-major + skew layout.
  static constexpr bool kUseFragmentBSharedLayout = (WarpMmaTilesNValue == 12);
  static constexpr int kBSharedFragments = kTensorBlockN / kWmmaN;
  static constexpr int kBSharedFragmentStride = kWmmaN;
  static constexpr int kBSharedFragmentElems = kWmmaK * kBSharedFragmentStride;
  static constexpr int kBSharedStride = kTensorBlockN + kAsyncCopyElems;
  static constexpr int kBSharedTileElems =
      kUseFragmentBSharedLayout ? (kBSharedFragments * kBSharedFragmentElems)
                                : (kWmmaK * kBSharedStride);
  static constexpr int kBStagedTileElems = kWmmaK * kTensorBlockN;
  static constexpr int kAAsyncCopiesPerRow = kWmmaK / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerRow = kTensorBlockN / kAsyncCopyElems;
  static constexpr int kAAsyncCopiesPerTile = kASharedTileElems / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerTile = kBStagedTileElems / kAsyncCopyElems;
};

using TensorCoreTile32 = TensorCoreTileConfig<1>;
using TensorCoreTile64 = TensorCoreTileConfig<2>;
using TensorCoreTile96 = TensorCoreTileConfig<3>;
using TensorCoreTile128 = TensorCoreTileConfig<4>;
using TensorCoreTile160 = TensorCoreTileConfig<5>;
using TensorCoreTile192 = TensorCoreTileConfig<6>;
using TensorCoreTile256 = TensorCoreTileConfig<8>;
using TensorCoreTile320 = TensorCoreTileConfig<10>;
using TensorCoreTile384 = TensorCoreTileConfig<12>;
using TensorCoreTile480 = TensorCoreTileConfig<15>;

constexpr int kFixedBenchmarkM = 6464;
constexpr int kFixedBenchmarkN = 7776;
constexpr int kFixedBenchmarkK = 7232;
constexpr int kFixedTailRegionN = TensorCoreTile96::kTensorBlockN;
constexpr int kFixedHotBandN = kFixedBenchmarkN - kFixedTailRegionN;
constexpr int kDefaultFixedMainTileN = TensorCoreTile384::kTensorBlockN;
constexpr int kLegacyFixedMainRegionN = 7296;
constexpr int kLegacyFixedMiddleRegionN = 384;
constexpr const char* kFixedMainTileEnvVar = "MATMUL_FIXED_MAIN_TILE_N";

static_assert(kAsyncCopyBytes == 16, "Tensor-core staging expects 16-byte async copies.");
static_assert(TensorCoreTile128::kTensorBlockM == 64, "Middle path expects a fixed 64x128 CTA tile.");
static_assert(TensorCoreTile128::kTensorBlockN == 128, "Middle path expects a fixed 64x128 CTA tile.");
static_assert(TensorCoreTile128::kWarpsPerBlock == 8, "Middle path expects an 8-warp CTA.");
static_assert(TensorCoreTile192::kTensorBlockM == 64, "Main path expects a fixed 64x192 CTA tile.");
static_assert(TensorCoreTile192::kTensorBlockN == 192, "Main path expects a fixed 64x192 CTA tile.");
static_assert(TensorCoreTile192::kWarpsPerBlock == 8, "Main path expects an 8-warp CTA.");
static_assert(TensorCoreTile96::kTensorBlockM == 64, "Tail path expects a fixed 64x96 CTA tile.");
static_assert(TensorCoreTile96::kTensorBlockN == 96, "Tail path expects a fixed 64x96 CTA tile.");
static_assert(TensorCoreTile96::kWarpsPerBlock == 8, "Tail path expects an 8-warp CTA.");
static_assert(TensorCoreTile160::kTensorBlockM == 64, "Main path expects a fixed 64x160 CTA tile.");
static_assert(TensorCoreTile160::kTensorBlockN == 160, "Main path expects a fixed 64x160 CTA tile.");
static_assert(TensorCoreTile160::kWarpsPerBlock == 8, "Main path expects an 8-warp CTA.");
static_assert(TensorCoreTile32::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile64::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile256::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile320::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile384::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile480::kTensorBlockM == 64, "Autotune candidates expect a fixed 64-row CTA tile.");
static_assert(TensorCoreTile32::kTensorBlockN == 32, "Autotune candidates expect a 64x32 CTA tile.");
static_assert(TensorCoreTile64::kTensorBlockN == 64, "Autotune candidates expect a 64x64 CTA tile.");
static_assert(TensorCoreTile256::kTensorBlockN == 256, "Autotune candidates expect a 64x256 CTA tile.");
static_assert(TensorCoreTile320::kTensorBlockN == 320, "Autotune candidates expect a 64x320 CTA tile.");
static_assert(TensorCoreTile384::kTensorBlockN == 384, "Autotune candidates expect a 64x384 CTA tile.");
static_assert(TensorCoreTile480::kTensorBlockN == 480, "Autotune candidates expect a 64x480 CTA tile.");
static_assert((kWmmaK % kAsyncCopyElems) == 0, "A tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile32::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile64::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kTensorBlockN % kAsyncCopyElems) == 0, "Middle B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile192::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kTensorBlockN % kAsyncCopyElems) == 0, "Tail B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile160::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile256::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile320::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile384::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile480::kTensorBlockN % kAsyncCopyElems) == 0, "Main B tile width must stay 16-byte aligned.");
static_assert((TensorCoreTile32::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile64::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kWarpGroupCols % kAsyncCopyElems) == 0, "Middle warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile192::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kWarpGroupCols % kAsyncCopyElems) == 0, "Tail warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile160::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile256::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile320::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile384::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile480::kWarpGroupCols % kAsyncCopyElems) == 0, "Main warp-group span must stay 16-byte aligned.");
static_assert((TensorCoreTile32::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile64::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile128::kBSharedStride % kAsyncCopyElems) == 0, "Middle B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile192::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kBSharedStride % kAsyncCopyElems) == 0, "Tail B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile160::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile256::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile320::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile384::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile480::kBSharedStride % kAsyncCopyElems) == 0, "Main B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kASharedTileElems % kAsyncCopyElems) == 0, "A tile must be divisible by async copy width.");
static_assert((TensorCoreTile32::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile64::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile128::kBSharedTileElems % kAsyncCopyElems) == 0, "Middle B tile must be divisible by async copy width.");
static_assert((TensorCoreTile192::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile96::kBSharedTileElems % kAsyncCopyElems) == 0, "Tail B tile must be divisible by async copy width.");
static_assert((TensorCoreTile160::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile256::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile320::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile384::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((TensorCoreTile480::kBSharedTileElems % kAsyncCopyElems) == 0, "Main B tile must be divisible by async copy width.");
static_assert((kLegacyFixedMainRegionN % TensorCoreTile192::kTensorBlockN) == 0, "Legacy fixed-shape main region must be an even count of 64x192 CTAs.");
static_assert((kLegacyFixedMiddleRegionN % TensorCoreTile128::kTensorBlockN) == 0, "Legacy fixed-shape middle region must be an even count of 64x128 CTAs.");
static_assert(kLegacyFixedMainRegionN == 38 * TensorCoreTile192::kTensorBlockN, "Legacy fixed-shape main region must cover 38 64x192 CTAs.");
static_assert(kLegacyFixedMiddleRegionN == 3 * TensorCoreTile128::kTensorBlockN, "Legacy fixed-shape middle region must cover 3 64x128 CTAs.");
static_assert(kDefaultFixedMainTileN == TensorCoreTile384::kTensorBlockN, "Autotune-selected default main tile must stay in sync with the promoted winner.");
static_assert(kFixedHotBandN == 7680, "Autotune hot band must cover 7680 columns.");
static_assert((kFixedHotBandN % TensorCoreTile32::kTensorBlockN) == 0, "64x32 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile64::kTensorBlockN) == 0, "64x64 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile96::kTensorBlockN) == 0, "64x96 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile128::kTensorBlockN) == 0, "64x128 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile160::kTensorBlockN) == 0, "64x160 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile192::kTensorBlockN) == 0, "64x192 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile256::kTensorBlockN) == 0, "64x256 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile320::kTensorBlockN) == 0, "64x320 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile384::kTensorBlockN) == 0, "64x384 main tile must divide the fixed hot band.");
static_assert((kFixedHotBandN % TensorCoreTile480::kTensorBlockN) == 0, "64x480 main tile must divide the fixed hot band.");
static_assert(kLegacyFixedMainRegionN + kLegacyFixedMiddleRegionN + kFixedTailRegionN == kFixedBenchmarkN, "Legacy main/middle/tail split must cover the fixed benchmark width exactly.");
static_assert(kFixedHotBandN + kFixedTailRegionN == kFixedBenchmarkN, "Hot-band plus tail split must cover the fixed benchmark width exactly.");
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
__host__ __device__ __forceinline__ int b_shared_offset_from_logical(int row, int logical_col) {
  if constexpr (TileConfig::kUseFragmentBSharedLayout) {
    const int fragment_idx = logical_col / kWmmaN;
    const int fragment_col = logical_col % kWmmaN;
    return fragment_idx * TileConfig::kBSharedFragmentElems +
           row * TileConfig::kBSharedFragmentStride +
           fragment_col;
  } else {
    return row * TileConfig::kBSharedStride + b_shared_col_from_logical<TileConfig>(logical_col);
  }
}

template <typename TileConfig>
__host__ __device__ __forceinline__ int b_shared_fragment_stride() {
  if constexpr (TileConfig::kUseFragmentBSharedLayout) {
    return TileConfig::kBSharedFragmentStride;
  } else {
    return TileConfig::kBSharedStride;
  }
}

template <typename TileConfig>
__device__ __forceinline__ const __nv_bfloat16* b_shared_fragment_ptr(
    const __nv_bfloat16* shared_tile,
    int warp_tile_n,
    int tile_n) {
  if constexpr (TileConfig::kUseFragmentBSharedLayout) {
    const int fragment_idx = warp_tile_n * TileConfig::kWarpMmaTilesN + tile_n;
    return shared_tile + fragment_idx * TileConfig::kBSharedFragmentElems;
  } else {
    const int logical_col = warp_tile_n * TileConfig::kWarpGroupCols + tile_n * kWmmaN;
    return shared_tile + b_shared_col_from_logical<TileConfig>(logical_col);
  }
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
    const int shared_offset = b_shared_offset_from_logical<TileConfig>(row, logical_col);
    cp_async_copy_16_bytes(
        shared_tile + shared_offset,
        global_tile + row * global_stride + logical_col);
  }
}

__host__ __device__ __forceinline__ int ceil_div(int value, int divisor) {
  return (value + divisor - 1) / divisor;
}

template <typename TileConfig>
__global__ void bf16_gemm_v1_tensor_core_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k);

template <typename TileConfig>
void launch_tensor_core_region(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k,
    int region_n,
    cudaStream_t stream) {
  const dim3 block(TileConfig::kWarpsPerBlock * kWarpSize, 1, 1);
  const dim3 grid(region_n / TileConfig::kTensorBlockN, m / TileConfig::kTensorBlockM, 1);
  bf16_gemm_v1_tensor_core_kernel<TileConfig><<<grid, block, 0, stream>>>(a, b, c, m, n, k);
}

int parse_fixed_main_tile_n_override() {
  const char* raw_value = std::getenv(kFixedMainTileEnvVar);
  if (raw_value == nullptr || raw_value[0] == '\0') {
    return 0;
  }

  char* parse_end = nullptr;
  const long parsed_value = std::strtol(raw_value, &parse_end, 10);
  if (parse_end == raw_value || *parse_end != '\0' ||
      parsed_value <= 0 || parsed_value > std::numeric_limits<int>::max()) {
    std::fprintf(stderr,
                 "Unsupported %s value '%s'; expected one of 32, 64, 96, 128, 160, 192, 256, 320, 384, 480.\n",
                 kFixedMainTileEnvVar,
                 raw_value);
    return -1;
  }

  return static_cast<int>(parsed_value);
}

bool launch_fixed_hot_band_by_tile_n(
    int tile_n,
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int m,
    int n,
    int k,
    cudaStream_t stream) {
  switch (tile_n) {
    case TensorCoreTile32::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile32>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile64::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile64>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile96::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile96>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile128::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile128>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile160::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile160>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile192::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile192>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile256::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile256>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile320::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile320>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile384::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile384>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    case TensorCoreTile480::kTensorBlockN:
      launch_tensor_core_region<TensorCoreTile480>(a, b, c, m, n, k, kFixedHotBandN, stream);
      return true;
    default:
      std::fprintf(stderr,
                   "Unsupported %s value '%d'; expected one of 32, 64, 96, 128, 160, 192, 256, 320, 384, 480.\n",
                   kFixedMainTileEnvVar,
                   tile_n);
      return false;
  }
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
    const int b_fragment_stride = b_shared_fragment_stride<TileConfig>();

    wmma::load_matrix_sync(a_frag, a_tile, kWmmaK);
    #pragma unroll
    for (int tile_n = 0; tile_n < TileConfig::kWarpMmaTilesN; ++tile_n) {
      const __nv_bfloat16* b_frag_tile =
          b_shared_fragment_ptr<TileConfig>(b_shared[curr_stage], warp_tile_n, tile_n);
      wmma::load_matrix_sync(b_frags[tile_n], b_frag_tile, b_fragment_stride);
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
    const int fixed_main_tile_n = parse_fixed_main_tile_n_override();
    if (fixed_main_tile_n < 0) {
      return false;
    }

    if (fixed_main_tile_n > 0) {
      if (!launch_fixed_hot_band_by_tile_n(fixed_main_tile_n, a, b, c, m, n, k, stream)) {
        return false;
      }

      launch_tensor_core_region<TensorCoreTile96>(
          a,
          b + kFixedHotBandN,
          c + kFixedHotBandN,
          m,
          n,
          k,
          kFixedTailRegionN,
          stream);
    } else {
      if (!launch_fixed_hot_band_by_tile_n(kDefaultFixedMainTileN, a, b, c, m, n, k, stream)) {
        return false;
      }

      launch_tensor_core_region<TensorCoreTile96>(
          a,
          b + kFixedHotBandN,
          c + kFixedHotBandN,
          m,
          n,
          k,
          kFixedTailRegionN,
          stream);
    }
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
