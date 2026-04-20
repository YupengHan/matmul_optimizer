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
constexpr int kEpilogueQuadElems = 4;
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
  static constexpr int kStaticSharedByteBudget = 48 * 1024;
  static constexpr int kASharedBytes = 2 * kASharedTileElems * sizeof(__nv_bfloat16);
  static constexpr int kCSharedTileBytesPerWarp = kCSharedTileElemsPerWarp * sizeof(float);
  static constexpr int kWarpGroupCols = kWarpMmaTilesN * kWmmaN;
  // Keep the B tile row-major for WMMA, but place a single 16-byte skew
  // between the two warp groups so each warp still reads a local slice.
  static constexpr int kBSharedStride = kTensorBlockN + kAsyncCopyElems;
  static constexpr int kBSharedTileElems = kWmmaK * kBSharedStride;
  static constexpr int kBSharedBytes = 2 * kBSharedTileElems * sizeof(__nv_bfloat16);
  // Two scratch stages let the hot epilogue reuse the alternate tile and skip
  // the extra warp sync that only protects the next store from clobbering the
  // current tile's shared export buffer.
  static constexpr int kCSharedStageCount =
      (kASharedBytes + kBSharedBytes +
       2 * kWarpsPerBlock * kCSharedTileBytesPerWarp <= kStaticSharedByteBudget)
          ? 2
          : 1;
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

struct FixedHotBandTile256x128 {
  static constexpr int kWarpTilesM = kTensorWarpTilesM;
  static constexpr int kWarpTilesN = kTensorWarpTilesN;
  static constexpr int kWarpMmaTilesM = 4;
  static constexpr int kWarpMmaTilesN = 4;
  static constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
  static constexpr int kWarpTileM = kWarpMmaTilesM * kWmmaM;
  static constexpr int kWarpTileN = kWarpMmaTilesN * kWmmaN;
  static constexpr int kTensorBlockM = kWarpTilesM * kWarpTileM;
  static constexpr int kTensorBlockN = kWarpTilesN * kWarpTileN;
  static constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
  static constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
  static constexpr int kStaticSharedByteBudget = 48 * 1024;
  static constexpr int kASharedBytes = 2 * kASharedTileElems * sizeof(__nv_bfloat16);
  static constexpr int kCSharedTileBytesPerWarp = kCSharedTileElemsPerWarp * sizeof(float);
  static constexpr int kWarpGroupCols = kWarpTileN;
  static constexpr int kBSharedStride = kTensorBlockN + kAsyncCopyElems;
  static constexpr int kBSharedTileElems = kWmmaK * kBSharedStride;
  static constexpr int kBSharedBytes = 2 * kBSharedTileElems * sizeof(__nv_bfloat16);
  static constexpr int kCSharedStageCount = 2;
  static constexpr int kBStagedTileElems = kWmmaK * kTensorBlockN;
  static constexpr int kAAsyncCopiesPerRow = kWmmaK / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerRow = kTensorBlockN / kAsyncCopyElems;
  static constexpr int kAAsyncCopiesPerTile = kASharedTileElems / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerTile = kBStagedTileElems / kAsyncCopyElems;
};

struct FixedHotBandTile128x128 {
  static constexpr int kWarpTilesM = 2;
  static constexpr int kWarpTilesN = 2;
  static constexpr int kWarpMmaTilesM = 4;
  static constexpr int kWarpMmaTilesN = 4;
  static constexpr int kWarpsPerBlock = kWarpTilesM * kWarpTilesN;
  static constexpr int kWarpTileM = kWarpMmaTilesM * kWmmaM;
  static constexpr int kWarpTileN = kWarpMmaTilesN * kWmmaN;
  static constexpr int kTensorBlockM = kWarpTilesM * kWarpTileM;
  static constexpr int kTensorBlockN = kWarpTilesN * kWarpTileN;
  static constexpr int kASharedTileElems = kTensorBlockM * kWmmaK;
  static constexpr int kCSharedTileElemsPerWarp = kWmmaM * kWmmaN;
  static constexpr int kStaticSharedByteBudget = 48 * 1024;
  static constexpr int kASharedBytes = 4 * kASharedTileElems * sizeof(__nv_bfloat16);
  static constexpr int kCSharedTileBytesPerWarp = kCSharedTileElemsPerWarp * sizeof(float);
  static constexpr int kWarpGroupCols = kWarpTileN;
  static constexpr int kBSharedStride = kTensorBlockN + kAsyncCopyElems;
  static constexpr int kBSharedTileElems = kWmmaK * kBSharedStride;
  static constexpr int kBSharedBytes = 4 * kBSharedTileElems * sizeof(__nv_bfloat16);
  static constexpr int kCSharedStageCount = 2;
  static constexpr int kBStagedTileElems = kWmmaK * kTensorBlockN;
  static constexpr int kAAsyncCopiesPerRow = kWmmaK / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerRow = kTensorBlockN / kAsyncCopyElems;
  static constexpr int kAAsyncCopiesPerTile = kASharedTileElems / kAsyncCopyElems;
  static constexpr int kBAsyncCopiesPerTile = kBStagedTileElems / kAsyncCopyElems;
};

struct FixedHotBandTile128x128PtxExportScratch {
  static constexpr int kPadFloatsPerRow = kEpilogueQuadElems;
  static constexpr int kLeadingDim = kWmmaN + kPadFloatsPerRow;
  static constexpr int kTileElemsPerWarp = kWmmaM * kLeadingDim;
  static constexpr int kStageCount = FixedHotBandTile128x128::kCSharedStageCount;
  static constexpr int kStageStride =
      FixedHotBandTile128x128::kWarpsPerBlock * kTileElemsPerWarp;
  static constexpr int kTotalElems = kStageCount * kStageStride;
  static constexpr int kSharedBytes = kTotalElems * sizeof(float);
};

constexpr int kFixedBenchmarkM = 6464;
constexpr int kFixedBenchmarkN = 7776;
constexpr int kFixedBenchmarkK = 7232;
constexpr int kFixedBenchmarkKTiles = kFixedBenchmarkK / kWmmaK;
constexpr int kHotBandStageKTiles = 2;
constexpr int kFixedBenchmarkKStages32 = kFixedBenchmarkKTiles / kHotBandStageKTiles;
constexpr int kFixedTailRegionN = TensorCoreTile96::kTensorBlockN;
constexpr int kFixedHotBandN = kFixedBenchmarkN - kFixedTailRegionN;
constexpr int kDefaultFixedMainTileN = TensorCoreTile384::kTensorBlockN;
constexpr int kFixedPivotHotRows = 6400;
constexpr int kFixedResidualHotRows = kFixedBenchmarkM - kFixedPivotHotRows;
constexpr int kFixedHotBandGroupedRows = 4;
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
static_assert(FixedHotBandTile256x128::kTensorBlockM == 256,
              "The fixed-shape pivot branch expects a 256-row CTA tile.");
static_assert(FixedHotBandTile256x128::kTensorBlockN == 128,
              "The fixed-shape pivot branch expects a 128-column CTA tile.");
static_assert(FixedHotBandTile256x128::kWarpsPerBlock == 8,
              "The fixed-shape pivot branch expects an 8-warp CTA.");
static_assert(FixedHotBandTile256x128::kWarpTileM == 64,
              "The fixed-shape pivot branch expects a 64x64 warp tile.");
static_assert(FixedHotBandTile256x128::kWarpTileN == 64,
              "The fixed-shape pivot branch expects a 64x64 warp tile.");
static_assert(FixedHotBandTile256x128::kCSharedStageCount == 2,
              "The pivot branch expects paired per-warp export scratch tiles.");
static_assert(FixedHotBandTile128x128::kTensorBlockM == 128,
              "The CUTLASS-shaped hot-band branch expects a 128-row CTA tile.");
static_assert(FixedHotBandTile128x128::kTensorBlockN == 128,
              "The CUTLASS-shaped hot-band branch expects a 128-column CTA tile.");
static_assert(FixedHotBandTile128x128::kWarpsPerBlock == 4,
              "The CUTLASS-shaped hot-band branch expects a 4-warp CTA.");
static_assert(FixedHotBandTile128x128::kWarpTileM == 64,
              "The CUTLASS-shaped hot-band branch expects a 64x64 warp tile.");
static_assert(FixedHotBandTile128x128::kWarpTileN == 64,
              "The CUTLASS-shaped hot-band branch expects a 64x64 warp tile.");
static_assert(FixedHotBandTile128x128::kCSharedStageCount == 2,
              "The CUTLASS-shaped hot-band branch expects paired per-warp export scratch tiles.");
static_assert((FixedHotBandTile128x128PtxExportScratch::kLeadingDim % kEpilogueQuadElems) == 0,
              "The PTX hot-band export scratch stride must stay quad-aligned.");
static_assert(((FixedHotBandTile128x128PtxExportScratch::kLeadingDim * sizeof(float)) % 16) == 0,
              "The PTX hot-band export scratch rows must stay 16-byte aligned.");
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
static_assert((FixedHotBandTile256x128::kTensorBlockN % kAsyncCopyElems) == 0,
              "The pivot hot-band B tile width must stay 16-byte aligned.");
static_assert((FixedHotBandTile128x128::kTensorBlockN % kAsyncCopyElems) == 0,
              "The CUTLASS-shaped hot-band B tile width must stay 16-byte aligned.");
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
static_assert((FixedHotBandTile256x128::kWarpGroupCols % kAsyncCopyElems) == 0,
              "The pivot hot-band warp-group span must stay 16-byte aligned.");
static_assert((FixedHotBandTile128x128::kWarpGroupCols % kAsyncCopyElems) == 0,
              "The CUTLASS-shaped hot-band warp-group span must stay 16-byte aligned.");
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
static_assert((FixedHotBandTile256x128::kBSharedStride % kAsyncCopyElems) == 0,
              "The pivot hot-band B shared stride must stay 16-byte aligned.");
static_assert((FixedHotBandTile128x128::kBSharedStride % kAsyncCopyElems) == 0,
              "The CUTLASS-shaped hot-band B shared stride must stay 16-byte aligned.");
static_assert((TensorCoreTile96::kASharedTileElems % kAsyncCopyElems) == 0, "A tile must be divisible by async copy width.");
static_assert((FixedHotBandTile256x128::kASharedTileElems % kAsyncCopyElems) == 0,
              "The pivot hot-band A tile must be divisible by async copy width.");
static_assert((FixedHotBandTile128x128::kASharedTileElems % kAsyncCopyElems) == 0,
              "The CUTLASS-shaped hot-band A tile must be divisible by async copy width.");
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
static_assert((FixedHotBandTile256x128::kBSharedTileElems % kAsyncCopyElems) == 0,
              "The pivot hot-band B tile must be divisible by async copy width.");
static_assert((FixedHotBandTile128x128::kBSharedTileElems % kAsyncCopyElems) == 0,
              "The CUTLASS-shaped hot-band B tile must be divisible by async copy width.");
static_assert((kLegacyFixedMainRegionN % TensorCoreTile192::kTensorBlockN) == 0, "Legacy fixed-shape main region must be an even count of 64x192 CTAs.");
static_assert((kLegacyFixedMiddleRegionN % TensorCoreTile128::kTensorBlockN) == 0, "Legacy fixed-shape middle region must be an even count of 64x128 CTAs.");
static_assert(kLegacyFixedMainRegionN == 38 * TensorCoreTile192::kTensorBlockN, "Legacy fixed-shape main region must cover 38 64x192 CTAs.");
static_assert(kLegacyFixedMiddleRegionN == 3 * TensorCoreTile128::kTensorBlockN, "Legacy fixed-shape middle region must cover 3 64x128 CTAs.");
static_assert(kDefaultFixedMainTileN == TensorCoreTile384::kTensorBlockN, "Autotune-selected default main tile must stay in sync with the promoted winner.");
static_assert((kFixedBenchmarkK % kWmmaK) == 0, "Fixed benchmark K must stay aligned to the WMMA depth.");
static_assert(kFixedBenchmarkKTiles == 452, "Fixed benchmark peeled hot path expects 452 K-tiles.");
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
static_assert((kFixedHotBandN % FixedHotBandTile256x128::kTensorBlockN) == 0,
              "The pivot hot-band CTA width must divide the fixed hot band.");
static_assert((kFixedPivotHotRows % FixedHotBandTile256x128::kTensorBlockM) == 0,
              "The pivot hot-band CTA height must divide the first 6400 rows exactly.");
static_assert((kFixedHotBandN % FixedHotBandTile128x128::kTensorBlockN) == 0,
              "The CUTLASS-shaped hot-band CTA width must divide the fixed hot band.");
static_assert((kFixedPivotHotRows % FixedHotBandTile128x128::kTensorBlockM) == 0,
              "The CUTLASS-shaped hot-band CTA height must divide the first 6400 rows exactly.");
static_assert((kFixedResidualHotRows % TensorCoreTile384::kTensorBlockM) == 0,
              "The stable remainder path must cover the last 64 rows exactly.");
static_assert(FixedHotBandTile256x128::kASharedBytes +
                      FixedHotBandTile256x128::kBSharedBytes +
                      FixedHotBandTile256x128::kCSharedStageCount *
                          FixedHotBandTile256x128::kWarpsPerBlock *
                          FixedHotBandTile256x128::kCSharedTileBytesPerWarp <=
                  FixedHotBandTile256x128::kStaticSharedByteBudget,
              "The pivot hot-band shared-memory budget must fit on sm86.");
static_assert(FixedHotBandTile128x128::kASharedBytes +
                      FixedHotBandTile128x128::kBSharedBytes +
                      FixedHotBandTile128x128::kCSharedStageCount *
                          FixedHotBandTile128x128::kWarpsPerBlock *
                          FixedHotBandTile128x128::kCSharedTileBytesPerWarp <=
                  FixedHotBandTile128x128::kStaticSharedByteBudget,
              "The CUTLASS-shaped hot-band shared-memory budget must fit on sm86.");
static_assert(2 * FixedHotBandTile128x128::kASharedTileElems * sizeof(__nv_bfloat16) +
                      2 * FixedHotBandTile128x128::kBSharedTileElems * sizeof(__nv_bfloat16) +
                      FixedHotBandTile128x128PtxExportScratch::kSharedBytes <=
                  FixedHotBandTile128x128::kStaticSharedByteBudget,
              "The PTX hot-band padded export scratch must fit inside the shared-memory budget.");
static_assert((kFixedBenchmarkKTiles % kHotBandStageKTiles) == 0,
              "The CUTLASS-shaped hot-band branch expects K to be divisible by 32.");
static_assert(kLegacyFixedMainRegionN + kLegacyFixedMiddleRegionN + kFixedTailRegionN == kFixedBenchmarkN, "Legacy main/middle/tail split must cover the fixed benchmark width exactly.");
static_assert(kFixedHotBandN + kFixedTailRegionN == kFixedBenchmarkN, "Hot-band plus tail split must cover the fixed benchmark width exactly.");
static_assert((kWmmaN % kEpilogueVecElems) == 0, "Epilogue vector stores require adjacent column pairs.");
static_assert((kWmmaN % kEpilogueQuadElems) == 0, "Quad epilogue stores require adjacent groups of four columns.");

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

__device__ __forceinline__ void cp_async_wait_group_1() {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  asm volatile("cp.async.wait_group 1;\n" ::);
#endif
}

__device__ __forceinline__ void store_bfloat162_pair(
    __nv_bfloat16* dst,
    const float2 values) {
  *reinterpret_cast<__nv_bfloat162*>(dst) = __float22bfloat162_rn(values);
}

__device__ __forceinline__ void store_bfloat164_quad(
    __nv_bfloat16* dst,
    const float4 values) {
  union PackedBfloat164 {
    int2 words;
    __nv_bfloat162 pairs[2];
  };
  PackedBfloat164 packed{};
  packed.pairs[0] = __float22bfloat162_rn(make_float2(values.x, values.y));
  packed.pairs[1] = __float22bfloat162_rn(make_float2(values.z, values.w));
  *reinterpret_cast<int2*>(dst) = packed.words;
}

struct PtxWmmaBf16Fragment {
  unsigned int reg[4];
};

struct PtxWmmaAccFragment {
  float reg[8];
};

struct PtxWmmaAccTileSet384 {
  PtxWmmaAccFragment tile0;
  PtxWmmaAccFragment tile1;
  PtxWmmaAccFragment tile2;
  PtxWmmaAccFragment tile3;
  PtxWmmaAccFragment tile4;
  PtxWmmaAccFragment tile5;
  PtxWmmaAccFragment tile6;
  PtxWmmaAccFragment tile7;
  PtxWmmaAccFragment tile8;
  PtxWmmaAccFragment tile9;
  PtxWmmaAccFragment tile10;
  PtxWmmaAccFragment tile11;
};

struct PtxWmmaAccTileSet64x64 {
  PtxWmmaAccFragment tile[FixedHotBandTile256x128::kWarpMmaTilesM *
                          FixedHotBandTile256x128::kWarpMmaTilesN];
};

__device__ __forceinline__ void ptx_wmma_fill_zero(PtxWmmaAccFragment& frag) {
  #pragma unroll
  for (int i = 0; i < 8; ++i) {
    frag.reg[i] = 0.0f;
  }
}

__device__ __forceinline__ void ptx_wmma_load_a_row(
    PtxWmmaBf16Fragment& frag,
    const __nv_bfloat16* shared_tile,
    int leading_dim) {
  const unsigned long long shared_addr = __cvta_generic_to_shared(shared_tile);
  asm volatile(
      "wmma.load.a.sync.aligned.row.m16n16k16.shared.bf16 "
      "{%0, %1, %2, %3}, [%4], %5;\n"
      : "=r"(frag.reg[0]), "=r"(frag.reg[1]), "=r"(frag.reg[2]), "=r"(frag.reg[3])
      : "l"(shared_addr), "r"(leading_dim));
}

__device__ __forceinline__ void ptx_wmma_load_b_row(
    PtxWmmaBf16Fragment& frag,
    const __nv_bfloat16* shared_tile,
    int leading_dim) {
  const unsigned long long shared_addr = __cvta_generic_to_shared(shared_tile);
  asm volatile(
      "wmma.load.b.sync.aligned.row.m16n16k16.shared.bf16 "
      "{%0, %1, %2, %3}, [%4], %5;\n"
      : "=r"(frag.reg[0]), "=r"(frag.reg[1]), "=r"(frag.reg[2]), "=r"(frag.reg[3])
      : "l"(shared_addr), "r"(leading_dim));
}

__device__ __forceinline__ void ptx_wmma_mma_row_row(
    PtxWmmaAccFragment& acc_frag,
    const PtxWmmaBf16Fragment& a_frag,
    const PtxWmmaBf16Fragment& b_frag) {
  asm volatile(
      "wmma.mma.sync.aligned.row.row.m16n16k16.f32.bf16.bf16.f32 "
      "{%0, %1, %2, %3, %4, %5, %6, %7}, "
      "{%8, %9, %10, %11}, "
      "{%12, %13, %14, %15}, "
      "{%0, %1, %2, %3, %4, %5, %6, %7};\n"
      : "+f"(acc_frag.reg[0]), "+f"(acc_frag.reg[1]), "+f"(acc_frag.reg[2]), "+f"(acc_frag.reg[3]),
        "+f"(acc_frag.reg[4]), "+f"(acc_frag.reg[5]), "+f"(acc_frag.reg[6]), "+f"(acc_frag.reg[7])
      : "r"(a_frag.reg[0]), "r"(a_frag.reg[1]), "r"(a_frag.reg[2]), "r"(a_frag.reg[3]),
        "r"(b_frag.reg[0]), "r"(b_frag.reg[1]), "r"(b_frag.reg[2]), "r"(b_frag.reg[3]));
}

__device__ __forceinline__ void ptx_wmma_store_d_row_shared(
    float* shared_tile,
    const PtxWmmaAccFragment& frag,
    int leading_dim) {
  const unsigned int shared_addr =
      static_cast<unsigned int>(__cvta_generic_to_shared(shared_tile));
  asm volatile(
      "wmma.store.d.sync.aligned.row.m16n16k16.shared.f32 "
      "[%0], {%1, %2, %3, %4, %5, %6, %7, %8}, %9;\n"
      :
      : "r"(shared_addr),
        "f"(frag.reg[0]), "f"(frag.reg[1]), "f"(frag.reg[2]), "f"(frag.reg[3]),
        "f"(frag.reg[4]), "f"(frag.reg[5]), "f"(frag.reg[6]), "f"(frag.reg[7]),
        "r"(leading_dim));
}

template <int TileIdx>
__device__ __forceinline__ PtxWmmaAccFragment& ptx_wmma_acc_tile(PtxWmmaAccTileSet384& tiles) {
  static_assert(TileIdx >= 0 && TileIdx < TensorCoreTile384::kWarpMmaTilesN,
                "Tile384 PTX accumulator index out of range.");
  if constexpr (TileIdx == 0) {
    return tiles.tile0;
  } else if constexpr (TileIdx == 1) {
    return tiles.tile1;
  } else if constexpr (TileIdx == 2) {
    return tiles.tile2;
  } else if constexpr (TileIdx == 3) {
    return tiles.tile3;
  } else if constexpr (TileIdx == 4) {
    return tiles.tile4;
  } else if constexpr (TileIdx == 5) {
    return tiles.tile5;
  } else if constexpr (TileIdx == 6) {
    return tiles.tile6;
  } else if constexpr (TileIdx == 7) {
    return tiles.tile7;
  } else if constexpr (TileIdx == 8) {
    return tiles.tile8;
  } else if constexpr (TileIdx == 9) {
    return tiles.tile9;
  } else if constexpr (TileIdx == 10) {
    return tiles.tile10;
  } else {
    return tiles.tile11;
  }
}

template <int TileIdx>
__device__ __forceinline__ const PtxWmmaAccFragment& ptx_wmma_acc_tile(
    const PtxWmmaAccTileSet384& tiles) {
  static_assert(TileIdx >= 0 && TileIdx < TensorCoreTile384::kWarpMmaTilesN,
                "Tile384 PTX accumulator index out of range.");
  if constexpr (TileIdx == 0) {
    return tiles.tile0;
  } else if constexpr (TileIdx == 1) {
    return tiles.tile1;
  } else if constexpr (TileIdx == 2) {
    return tiles.tile2;
  } else if constexpr (TileIdx == 3) {
    return tiles.tile3;
  } else if constexpr (TileIdx == 4) {
    return tiles.tile4;
  } else if constexpr (TileIdx == 5) {
    return tiles.tile5;
  } else if constexpr (TileIdx == 6) {
    return tiles.tile6;
  } else if constexpr (TileIdx == 7) {
    return tiles.tile7;
  } else if constexpr (TileIdx == 8) {
    return tiles.tile8;
  } else if constexpr (TileIdx == 9) {
    return tiles.tile9;
  } else if constexpr (TileIdx == 10) {
    return tiles.tile10;
  } else {
    return tiles.tile11;
  }
}

template <int TileRow, int TileCol>
__device__ __forceinline__ PtxWmmaAccFragment& ptx_wmma_acc_tile(
    PtxWmmaAccTileSet64x64& tiles) {
  static_assert(TileRow >= 0 && TileRow < FixedHotBandTile256x128::kWarpMmaTilesM,
                "64x64 PTX accumulator row index out of range.");
  static_assert(TileCol >= 0 && TileCol < FixedHotBandTile256x128::kWarpMmaTilesN,
                "64x64 PTX accumulator col index out of range.");
  return tiles.tile[TileRow * FixedHotBandTile256x128::kWarpMmaTilesN + TileCol];
}

template <int TileRow, int TileCol>
__device__ __forceinline__ const PtxWmmaAccFragment& ptx_wmma_acc_tile(
    const PtxWmmaAccTileSet64x64& tiles) {
  static_assert(TileRow >= 0 && TileRow < FixedHotBandTile256x128::kWarpMmaTilesM,
                "64x64 PTX accumulator row index out of range.");
  static_assert(TileCol >= 0 && TileCol < FixedHotBandTile256x128::kWarpMmaTilesN,
                "64x64 PTX accumulator col index out of range.");
  return tiles.tile[TileRow * FixedHotBandTile256x128::kWarpMmaTilesN + TileCol];
}

template <int TileIdx = 0>
__device__ __forceinline__ void ptx_wmma_fill_zero_tile_set(PtxWmmaAccTileSet384& tiles) {
  if constexpr (TileIdx < TensorCoreTile384::kWarpMmaTilesN) {
    ptx_wmma_fill_zero(ptx_wmma_acc_tile<TileIdx>(tiles));
    ptx_wmma_fill_zero_tile_set<TileIdx + 1>(tiles);
  }
}

template <int TileIdx = 0>
__device__ __forceinline__ void ptx_wmma_fill_zero_tile_set(PtxWmmaAccTileSet64x64& tiles) {
  if constexpr (TileIdx < FixedHotBandTile256x128::kWarpMmaTilesM *
                               FixedHotBandTile256x128::kWarpMmaTilesN) {
    ptx_wmma_fill_zero(tiles.tile[TileIdx]);
    ptx_wmma_fill_zero_tile_set<TileIdx + 1>(tiles);
  }
}

template <int Step>
struct PtxWmmaMirroredTileIndex384 {
  static_assert(Step >= 0 && Step < TensorCoreTile384::kWarpMmaTilesN,
                "Tile384 mirrored sweep step out of range.");
  static constexpr int kValue =
      (Step & 1) == 0 ? (Step / 2)
                      : (TensorCoreTile384::kWarpMmaTilesN - 1 - (Step / 2));
};

template <int Step = 0>
__device__ __forceinline__ void ptx_wmma_accumulate_tile_set_384(
    PtxWmmaAccTileSet384& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag,
    const __nv_bfloat16* b_tile) {
  if constexpr (Step < TensorCoreTile384::kWarpMmaTilesN) {
    constexpr int TileIdx = PtxWmmaMirroredTileIndex384<Step>::kValue;
    PtxWmmaBf16Fragment b_frag;
    ptx_wmma_load_b_row(
        b_frag,
        b_tile + TileIdx * kWmmaN,
        TensorCoreTile384::kBSharedStride);
    ptx_wmma_mma_row_row(ptx_wmma_acc_tile<TileIdx>(acc_tiles), a_frag, b_frag);
    ptx_wmma_accumulate_tile_set_384<Step + 1>(acc_tiles, a_frag, b_tile);
  }
}

template <int Step>
struct PtxWmmaMirroredTileIndex64x64 {
  static_assert(Step >= 0 && Step < FixedHotBandTile256x128::kWarpMmaTilesN,
                "64x64 mirrored sweep step out of range.");
  static constexpr int kValue =
      (Step & 1) == 0 ? (Step / 2)
                      : (FixedHotBandTile256x128::kWarpMmaTilesN - 1 - (Step / 2));
};

template <int RowPairBase, int ColIdx>
__device__ __forceinline__ void ptx_wmma_mma_row_pair_col_64x64(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag0,
    const PtxWmmaBf16Fragment& a_frag1,
    const PtxWmmaBf16Fragment& b_frag) {
  static_assert(RowPairBase >= 0 &&
                    RowPairBase + 1 < FixedHotBandTile256x128::kWarpMmaTilesM,
                "64x64 row-pair MMA helper expects a valid 2-row pair.");
  static_assert(ColIdx >= 0 && ColIdx < FixedHotBandTile256x128::kWarpMmaTilesN,
                "64x64 column index out of range.");
  ptx_wmma_mma_row_row(
      ptx_wmma_acc_tile<RowPairBase, ColIdx>(acc_tiles),
      a_frag0,
      b_frag);
  ptx_wmma_mma_row_row(
      ptx_wmma_acc_tile<RowPairBase + 1, ColIdx>(acc_tiles),
      a_frag1,
      b_frag);
}

template <int Step>
__device__ __forceinline__ void ptx_wmma_load_col_fragment_64x64(
    PtxWmmaBf16Fragment& b_frag,
    const __nv_bfloat16* b_tile) {
  constexpr int ColIdx = PtxWmmaMirroredTileIndex64x64<Step>::kValue;
  ptx_wmma_load_b_row(
      b_frag,
      b_tile + ColIdx * kWmmaN,
      FixedHotBandTile256x128::kBSharedStride);
}

template <int RowPairBase, int Step = 0>
__device__ __forceinline__ void ptx_wmma_accumulate_col_tiles_64x64_lookahead(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag0,
    const PtxWmmaBf16Fragment& a_frag1,
    const __nv_bfloat16* b_tile,
    const PtxWmmaBf16Fragment& current_b_frag) {
  if constexpr (Step < FixedHotBandTile256x128::kWarpMmaTilesN) {
    constexpr int ColIdx = PtxWmmaMirroredTileIndex64x64<Step>::kValue;
    if constexpr (Step + 1 < FixedHotBandTile256x128::kWarpMmaTilesN) {
      PtxWmmaBf16Fragment next_b_frag;
      // Keep one B fragment live so the next Ps2r load can issue ahead of the
      // current MMA pair without changing tile ownership or shared layout.
      ptx_wmma_load_col_fragment_64x64<Step + 1>(next_b_frag, b_tile);
      ptx_wmma_mma_row_pair_col_64x64<RowPairBase, ColIdx>(
          acc_tiles, a_frag0, a_frag1, current_b_frag);
      ptx_wmma_accumulate_col_tiles_64x64_lookahead<RowPairBase, Step + 1>(
          acc_tiles, a_frag0, a_frag1, b_tile, next_b_frag);
    } else {
      ptx_wmma_mma_row_pair_col_64x64<RowPairBase, ColIdx>(
          acc_tiles, a_frag0, a_frag1, current_b_frag);
    }
  }
}

template <int RowPairBase, int Step = 0>
__device__ __forceinline__ void ptx_wmma_accumulate_col_tiles_64x64(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag0,
    const PtxWmmaBf16Fragment& a_frag1,
    const __nv_bfloat16* b_tile) {
  if constexpr (Step < FixedHotBandTile256x128::kWarpMmaTilesN) {
    PtxWmmaBf16Fragment b_frag;
    ptx_wmma_load_col_fragment_64x64<Step>(b_frag, b_tile);
    ptx_wmma_accumulate_col_tiles_64x64_lookahead<RowPairBase, Step>(
        acc_tiles, a_frag0, a_frag1, b_tile, b_frag);
  }
}

template <int RowPairBase = 0>
__device__ __forceinline__ void ptx_wmma_accumulate_row_pairs_64x64(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const __nv_bfloat16* a_tile,
    const __nv_bfloat16* b_tile) {
  if constexpr (RowPairBase < FixedHotBandTile256x128::kWarpMmaTilesM) {
    PtxWmmaBf16Fragment a_frag0;
    PtxWmmaBf16Fragment a_frag1;
    ptx_wmma_load_a_row(
        a_frag0,
        a_tile + RowPairBase * kWmmaM * kWmmaK,
        kWmmaK);
    ptx_wmma_load_a_row(
        a_frag1,
        a_tile + (RowPairBase + 1) * kWmmaM * kWmmaK,
        kWmmaK);
    ptx_wmma_accumulate_col_tiles_64x64<RowPairBase>(
        acc_tiles, a_frag0, a_frag1, b_tile);
    ptx_wmma_accumulate_row_pairs_64x64<RowPairBase + 2>(
        acc_tiles, a_tile, b_tile);
  }
}

__device__ __forceinline__ void ptx_wmma_accumulate_tile_set_64x64(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const __nv_bfloat16* a_tile,
    const __nv_bfloat16* b_tile) {
  ptx_wmma_accumulate_row_pairs_64x64(acc_tiles, a_tile, b_tile);
}

template <int ColIdx>
__device__ __forceinline__ void ptx_wmma_mma_all_row_pairs_col_64x64_ptx_microkernel(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag0,
    const PtxWmmaBf16Fragment& a_frag1,
    const PtxWmmaBf16Fragment& a_frag2,
    const PtxWmmaBf16Fragment& a_frag3,
    const PtxWmmaBf16Fragment& b_frag) {
  static_assert(FixedHotBandTile128x128::kWarpMmaTilesM == 4,
                "The PTX hot-band microkernel expects a 64x64 warp tile.");
  ptx_wmma_mma_row_pair_col_64x64<0, ColIdx>(
      acc_tiles, a_frag0, a_frag1, b_frag);
  ptx_wmma_mma_row_pair_col_64x64<2, ColIdx>(
      acc_tiles, a_frag2, a_frag3, b_frag);
}

template <int Step = 0>
__device__ __forceinline__ void ptx_wmma_accumulate_col_tiles_64x64_ptx_microkernel(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const PtxWmmaBf16Fragment& a_frag0,
    const PtxWmmaBf16Fragment& a_frag1,
    const PtxWmmaBf16Fragment& a_frag2,
    const PtxWmmaBf16Fragment& a_frag3,
    const __nv_bfloat16* b_tile) {
  if constexpr (Step < FixedHotBandTile128x128::kWarpMmaTilesN) {
    constexpr int ColIdx = PtxWmmaMirroredTileIndex64x64<Step>::kValue;
    PtxWmmaBf16Fragment b_frag;
    // Load one mirrored-column B fragment, consume it across both row pairs,
    // then advance so the PTX-only branch no longer keeps a next-fragment
    // lookahead live through the recursive sweep.
    ptx_wmma_load_col_fragment_64x64<Step>(b_frag, b_tile);
    ptx_wmma_mma_all_row_pairs_col_64x64_ptx_microkernel<ColIdx>(
        acc_tiles, a_frag0, a_frag1, a_frag2, a_frag3, b_frag);
    ptx_wmma_accumulate_col_tiles_64x64_ptx_microkernel<Step + 1>(
        acc_tiles, a_frag0, a_frag1, a_frag2, a_frag3, b_tile);
  }
}

__device__ __forceinline__ void ptx_wmma_accumulate_tile_set_64x64_ptx_microkernel(
    PtxWmmaAccTileSet64x64& acc_tiles,
    const __nv_bfloat16* a_tile,
    const __nv_bfloat16* b_tile) {
  PtxWmmaBf16Fragment a_frag0;
  PtxWmmaBf16Fragment a_frag1;
  PtxWmmaBf16Fragment a_frag2;
  PtxWmmaBf16Fragment a_frag3;

  ptx_wmma_load_a_row(a_frag0, a_tile, kWmmaK);
  ptx_wmma_load_a_row(a_frag1, a_tile + kWmmaM * kWmmaK, kWmmaK);
  ptx_wmma_load_a_row(a_frag2, a_tile + 2 * kWmmaM * kWmmaK, kWmmaK);
  ptx_wmma_load_a_row(a_frag3, a_tile + 3 * kWmmaM * kWmmaK, kWmmaK);
  ptx_wmma_accumulate_col_tiles_64x64_ptx_microkernel(
      acc_tiles, a_frag0, a_frag1, a_frag2, a_frag3, b_tile);
}

template <typename TileConfig, int TileIdx = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_set_384(
    const PtxWmmaAccTileSet384& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  if constexpr (TileIdx < TensorCoreTile384::kWarpMmaTilesN) {
    constexpr int kCSharedStageStride =
        TileConfig::kWarpsPerBlock * TileConfig::kCSharedTileElemsPerWarp;
    constexpr int kCSharedStageMask = TileConfig::kCSharedStageCount - 1;
    float* warp_c_tile =
        c_shared + (TileIdx & kCSharedStageMask) * kCSharedStageStride +
        warp_id * TileConfig::kCSharedTileElemsPerWarp;
    ptx_wmma_store_d_row_shared(
        warp_c_tile, ptx_wmma_acc_tile<TileIdx>(acc_tiles), kWmmaN);
    __syncwarp();

    const float4* warp_c_tile_quads = reinterpret_cast<const float4*>(warp_c_tile);
    constexpr int kQuadsPerRow = kWmmaN / kEpilogueQuadElems;
    constexpr int kQuadsPerTile = TileConfig::kCSharedTileElemsPerWarp / kEpilogueQuadElems;

    #pragma unroll
    for (int quad_idx = lane_id; quad_idx < kQuadsPerTile; quad_idx += kWarpSize) {
      const int local_row = quad_idx / kQuadsPerRow;
      const int local_col = (quad_idx % kQuadsPerRow) * kEpilogueQuadElems;
      store_bfloat164_quad(
          c_tile_base + local_row * kFixedBenchmarkN + TileIdx * kWmmaN + local_col,
          warp_c_tile_quads[quad_idx]);
    }
    if constexpr (TileConfig::kCSharedStageCount == 1) {
      __syncwarp();
    }
    ptx_wmma_store_tile_set_384<TileConfig, TileIdx + 1>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
}

template <int TileIdx>
__device__ __forceinline__ void ptx_export_shared_tile_quads_384(
    const float* warp_c_tile,
    __nv_bfloat16* c_tile_base,
    int lane_id) {
  static_assert(TileIdx >= 0 && TileIdx < TensorCoreTile384::kWarpMmaTilesN,
                "Tile384 export tile index out of range.");
  const float4* warp_c_tile_quads = reinterpret_cast<const float4*>(warp_c_tile);
  constexpr int kQuadsPerRow = kWmmaN / kEpilogueQuadElems;
  constexpr int kQuadsPerTile = TensorCoreTile384::kCSharedTileElemsPerWarp / kEpilogueQuadElems;

  #pragma unroll
  for (int quad_idx = lane_id; quad_idx < kQuadsPerTile; quad_idx += kWarpSize) {
    const int local_row = quad_idx / kQuadsPerRow;
    const int local_col = (quad_idx % kQuadsPerRow) * kEpilogueQuadElems;
    store_bfloat164_quad(
        c_tile_base + local_row * kFixedBenchmarkN + TileIdx * kWmmaN + local_col,
        warp_c_tile_quads[quad_idx]);
  }
}

template <typename TileConfig, int TilePairBase = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_pairs_384(
    const PtxWmmaAccTileSet384& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  static_assert(TileConfig::kCSharedStageCount == 2,
                "Tile pair export batching requires the two-stage Tile384 c_shared scratch.");
  if constexpr (TilePairBase < TensorCoreTile384::kWarpMmaTilesN) {
    constexpr int kCSharedStageStride =
        TileConfig::kWarpsPerBlock * TileConfig::kCSharedTileElemsPerWarp;
    float* warp_c_tile_stage0 =
        c_shared + warp_id * TileConfig::kCSharedTileElemsPerWarp;
    float* warp_c_tile_stage1 =
        c_shared + kCSharedStageStride + warp_id * TileConfig::kCSharedTileElemsPerWarp;

    // Fill both c_shared stages before synchronizing so the two scratch tiles
    // are used as an actual pair instead of a per-tile ping-pong.
    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage0, ptx_wmma_acc_tile<TilePairBase>(acc_tiles), kWmmaN);
    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage1, ptx_wmma_acc_tile<TilePairBase + 1>(acc_tiles), kWmmaN);
    __syncwarp();

    ptx_export_shared_tile_quads_384<TilePairBase>(
        warp_c_tile_stage0, c_tile_base, lane_id);
    ptx_export_shared_tile_quads_384<TilePairBase + 1>(
        warp_c_tile_stage1, c_tile_base, lane_id);

    ptx_wmma_store_tile_pairs_384<TileConfig, TilePairBase + 2>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
}

template <int TileRow, int TileCol>
__device__ __forceinline__ void ptx_export_shared_tile_quads_64x64(
    const float* warp_c_tile,
    __nv_bfloat16* c_tile_base,
    int lane_id) {
  static_assert(TileRow >= 0 && TileRow < FixedHotBandTile256x128::kWarpMmaTilesM,
                "64x64 export tile row index out of range.");
  static_assert(TileCol >= 0 && TileCol < FixedHotBandTile256x128::kWarpMmaTilesN,
                "64x64 export tile col index out of range.");
  const float4* warp_c_tile_quads = reinterpret_cast<const float4*>(warp_c_tile);
  constexpr int kQuadsPerRow = kWmmaN / kEpilogueQuadElems;
  constexpr int kQuadsPerTile =
      FixedHotBandTile256x128::kCSharedTileElemsPerWarp / kEpilogueQuadElems;

  #pragma unroll
  for (int quad_idx = lane_id; quad_idx < kQuadsPerTile; quad_idx += kWarpSize) {
    const int local_row = quad_idx / kQuadsPerRow;
    const int local_col = (quad_idx % kQuadsPerRow) * kEpilogueQuadElems;
    store_bfloat164_quad(
        c_tile_base + TileRow * kWmmaM * kFixedBenchmarkN + TileCol * kWmmaN +
            local_row * kFixedBenchmarkN + local_col,
        warp_c_tile_quads[quad_idx]);
  }
}

template <int TileRow, int TileCol>
__device__ __forceinline__ void ptx_export_shared_tile_quads_64x64_ptx_microkernel(
    const float* warp_c_tile,
    __nv_bfloat16* c_tile_base,
    int lane_id) {
  static_assert(TileRow >= 0 && TileRow < FixedHotBandTile128x128::kWarpMmaTilesM,
                "PTX 64x64 export tile row index out of range.");
  static_assert(TileCol >= 0 && TileCol < FixedHotBandTile128x128::kWarpMmaTilesN,
                "PTX 64x64 export tile col index out of range.");
  constexpr int kQuadsPerRow = kWmmaN / kEpilogueQuadElems;
  constexpr int kQuadsPerTile = kWmmaM * kQuadsPerRow;

  #pragma unroll
  for (int quad_idx = lane_id; quad_idx < kQuadsPerTile; quad_idx += kWarpSize) {
    const int local_row = quad_idx / kQuadsPerRow;
    const int local_quad = quad_idx % kQuadsPerRow;
    const float4* warp_c_tile_row_quads = reinterpret_cast<const float4*>(
        warp_c_tile + local_row * FixedHotBandTile128x128PtxExportScratch::kLeadingDim);
    store_bfloat164_quad(
        c_tile_base + TileRow * kWmmaM * kFixedBenchmarkN + TileCol * kWmmaN +
            local_row * kFixedBenchmarkN + local_quad * kEpilogueQuadElems,
        warp_c_tile_row_quads[local_quad]);
  }
}

template <typename HotBandTileConfig, int TileRow, int TilePairColBase = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_row_pairs_64x64(
    const PtxWmmaAccTileSet64x64& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  static_assert(HotBandTileConfig::kCSharedStageCount == 2,
                "Paired 64x64 export requires two per-warp c_shared stages.");
  if constexpr (TilePairColBase < FixedHotBandTile256x128::kWarpMmaTilesN) {
    constexpr int kCSharedStageStride =
        HotBandTileConfig::kWarpsPerBlock *
        HotBandTileConfig::kCSharedTileElemsPerWarp;
    float* warp_c_tile_stage0 =
        c_shared + warp_id * HotBandTileConfig::kCSharedTileElemsPerWarp;
    float* warp_c_tile_stage1 =
        c_shared + kCSharedStageStride +
        warp_id * HotBandTileConfig::kCSharedTileElemsPerWarp;

    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage0,
        ptx_wmma_acc_tile<TileRow, TilePairColBase>(acc_tiles),
        kWmmaN);
    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage1,
        ptx_wmma_acc_tile<TileRow, TilePairColBase + 1>(acc_tiles),
        kWmmaN);
    __syncwarp();

    ptx_export_shared_tile_quads_64x64<TileRow, TilePairColBase>(
        warp_c_tile_stage0, c_tile_base, lane_id);
    ptx_export_shared_tile_quads_64x64<TileRow, TilePairColBase + 1>(
        warp_c_tile_stage1, c_tile_base, lane_id);

    ptx_wmma_store_tile_row_pairs_64x64<
        HotBandTileConfig,
        TileRow,
        TilePairColBase + 2>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
}

template <typename HotBandTileConfig, int TileRow = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_pairs_64x64(
    const PtxWmmaAccTileSet64x64& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  if constexpr (TileRow < FixedHotBandTile256x128::kWarpMmaTilesM) {
    ptx_wmma_store_tile_row_pairs_64x64<HotBandTileConfig, TileRow>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
    ptx_wmma_store_tile_pairs_64x64<HotBandTileConfig, TileRow + 1>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
}

template <int TileRow, int TilePairColBase = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel(
    const PtxWmmaAccTileSet64x64& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  static_assert(FixedHotBandTile128x128PtxExportScratch::kStageCount == 2,
                "PTX 64x64 paired export requires two per-warp c_shared stages.");
  if constexpr (TilePairColBase < FixedHotBandTile128x128::kWarpMmaTilesN) {
    float* warp_c_tile_stage0 =
        c_shared + warp_id * FixedHotBandTile128x128PtxExportScratch::kTileElemsPerWarp;
    float* warp_c_tile_stage1 =
        c_shared + FixedHotBandTile128x128PtxExportScratch::kStageStride +
        warp_id * FixedHotBandTile128x128PtxExportScratch::kTileElemsPerWarp;

    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage0,
        ptx_wmma_acc_tile<TileRow, TilePairColBase>(acc_tiles),
        FixedHotBandTile128x128PtxExportScratch::kLeadingDim);
    ptx_wmma_store_d_row_shared(
        warp_c_tile_stage1,
        ptx_wmma_acc_tile<TileRow, TilePairColBase + 1>(acc_tiles),
        FixedHotBandTile128x128PtxExportScratch::kLeadingDim);
    __syncwarp();

    ptx_export_shared_tile_quads_64x64_ptx_microkernel<TileRow, TilePairColBase>(
        warp_c_tile_stage0, c_tile_base, lane_id);
    ptx_export_shared_tile_quads_64x64_ptx_microkernel<TileRow, TilePairColBase + 1>(
        warp_c_tile_stage1, c_tile_base, lane_id);

    ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel<
        TileRow,
        TilePairColBase + 2>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
}

template <int TileRow = 0>
__device__ __forceinline__ void ptx_wmma_store_tile_pairs_64x64_ptx_microkernel(
    const PtxWmmaAccTileSet64x64& acc_tiles,
    float* c_shared,
    __nv_bfloat16* c_tile_base,
    int warp_id,
    int lane_id) {
  if constexpr (TileRow < FixedHotBandTile128x128::kWarpMmaTilesM) {
    ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel<TileRow>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
    ptx_wmma_store_tile_pairs_64x64_ptx_microkernel<TileRow + 1>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
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

__device__ __forceinline__ void stage_a_shared_tile_async_ptx_microkernel(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  static_assert(FixedHotBandTile128x128::kWarpsPerBlock == 4,
                "The PTX hot-band staging split expects a 4-warp CTA.");
  constexpr int kProducerThreads = 2 * kWarpSize;
  if (threadIdx.x >= kProducerThreads) {
    return;
  }

  // Keep the PTX branch's producer partitioning fixed: two warps feed A only.
  for (int copy_idx = threadIdx.x;
       copy_idx < FixedHotBandTile128x128::kAAsyncCopiesPerTile;
       copy_idx += kProducerThreads) {
    const int row = copy_idx / FixedHotBandTile128x128::kAAsyncCopiesPerRow;
    const int col =
        (copy_idx % FixedHotBandTile128x128::kAAsyncCopiesPerRow) * kAsyncCopyElems;
    cp_async_copy_16_bytes(
        shared_tile + row * kWmmaK + col,
        global_tile + row * global_stride + col);
  }
}

__device__ __forceinline__ void stage_b_shared_tile_async_ptx_microkernel(
    __nv_bfloat16* shared_tile,
    const __nv_bfloat16* global_tile,
    int global_stride) {
  static_assert(FixedHotBandTile128x128::kWarpsPerBlock == 4,
                "The PTX hot-band staging split expects a 4-warp CTA.");
  constexpr int kProducerThreads = 2 * kWarpSize;
  if (threadIdx.x < kProducerThreads) {
    return;
  }

  const int producer_thread_idx = threadIdx.x - kProducerThreads;
  for (int copy_idx = producer_thread_idx;
       copy_idx < FixedHotBandTile128x128::kBAsyncCopiesPerTile;
       copy_idx += kProducerThreads) {
    const int row = copy_idx / FixedHotBandTile128x128::kBAsyncCopiesPerRow;
    const int logical_col =
        (copy_idx % FixedHotBandTile128x128::kBAsyncCopiesPerRow) * kAsyncCopyElems;
    const int shared_col =
        b_shared_col_from_logical<FixedHotBandTile128x128>(logical_col);
    cp_async_copy_16_bytes(
        shared_tile + row * FixedHotBandTile128x128::kBSharedStride + shared_col,
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

template <typename TileConfig, int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_peeled_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int block_row_tile_base);

template <int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c);

template <int FixedKStages>
__global__ void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c);

template <int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c);

template <int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c);

template <typename TileConfig, int FixedKTiles>
void launch_fixed_peeled_hot_band_row_band(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int block_row_tile_base,
    int block_row_count,
    cudaStream_t stream) {
  bf16_gemm_v1_tensor_core_fixed_peeled_kernel<
      TileConfig,
      FixedKTiles><<<
          dim3(kFixedHotBandN / TileConfig::kTensorBlockN, block_row_count, 1),
          dim3(TileConfig::kWarpsPerBlock * kWarpSize, 1, 1),
          0,
          stream>>>(a, b, c, block_row_tile_base);
}

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
      launch_fixed_peeled_hot_band_row_band<
          TensorCoreTile384,
          kFixedBenchmarkKTiles>(
              a,
              b,
              c,
              0,
              kFixedBenchmarkM / TensorCoreTile384::kTensorBlockM,
              stream);
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
  __shared__ __align__(16)
      float c_shared[TileConfig::kCSharedStageCount * TileConfig::kWarpsPerBlock *
                     TileConfig::kCSharedTileElemsPerWarp];

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

  constexpr int kCSharedStageStride =
      TileConfig::kWarpsPerBlock * TileConfig::kCSharedTileElemsPerWarp;
  constexpr int kCSharedStageMask = TileConfig::kCSharedStageCount - 1;
  __nv_bfloat16* c_tile_base = c + row * n + col;
  #pragma unroll
  for (int tile_n = 0; tile_n < TileConfig::kWarpMmaTilesN; ++tile_n) {
    float* warp_c_tile =
        c_shared + (tile_n & kCSharedStageMask) * kCSharedStageStride +
        warp_id * TileConfig::kCSharedTileElemsPerWarp;
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
          c_tile_base + local_row * n + tile_n * kWmmaN + local_col,
          warp_c_tile_pairs[pair_idx]);
    }
    if constexpr (TileConfig::kCSharedStageCount == 1) {
      __syncwarp();
    }
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

template <typename TileConfig>
__device__ __forceinline__ void accumulate_peeled_shared_stage_ptx(
    PtxWmmaAccTileSet384& acc_tiles,
    const __nv_bfloat16* a_stage,
    const __nv_bfloat16* b_stage,
    int warp_tile_m,
    int warp_tile_n) {
  static_assert(TileConfig::kTensorBlockN == TensorCoreTile384::kTensorBlockN,
                "The Tile384 PTX accumulator helper is only valid on the hot-band kernel.");
  PtxWmmaBf16Fragment a_frag;

  const __nv_bfloat16* a_tile =
      a_stage + warp_tile_m * kWmmaM * kWmmaK;
  const __nv_bfloat16* b_tile =
      b_stage + b_shared_col_from_logical<TileConfig>(warp_tile_n * TileConfig::kWarpGroupCols);

  ptx_wmma_load_a_row(a_frag, a_tile, kWmmaK);
  ptx_wmma_accumulate_tile_set_384(acc_tiles, a_frag, b_tile);
}

template <typename TileConfig>
__device__ __forceinline__ void advance_peeled_hot_stage_ptx(
    PtxWmmaAccTileSet384& acc_tiles,
    __nv_bfloat16 a_shared[][TileConfig::kASharedTileElems],
    __nv_bfloat16 b_shared[][TileConfig::kBSharedTileElems],
    const __nv_bfloat16* a_block,
    const __nv_bfloat16* b_block,
    int future_tile_k,
    int warp_tile_m,
    int warp_tile_n,
    int& curr_stage,
    int& next_stage) {
  accumulate_peeled_shared_stage_ptx<TileConfig>(
      acc_tiles, a_shared[curr_stage], b_shared[curr_stage], warp_tile_m, warp_tile_n);

  // Collapse the recycle barrier and consumer-ready barrier into one steady-state
  // handoff: with only one pending group in flight here, we must fully wait for
  // the consumer stage before the single CTA sync publishes it and guarantees
  // the just-consumed stage is safe to refill.
  cp_async_wait_group_0();
  __syncthreads();

  stage_a_shared_tile_async<TileConfig>(
      a_shared[curr_stage], a_block + future_tile_k, kFixedBenchmarkK);
  stage_b_shared_tile_async<TileConfig>(
      b_shared[curr_stage],
      b_block + future_tile_k * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();

  const int consumed_stage = curr_stage;
  curr_stage = next_stage;
  next_stage = consumed_stage;
}

template <typename TileConfig, int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_peeled_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c,
    int block_row_tile_base) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  static_assert(FixedKTiles > 3, "Pairwise peeled fixed-shape kernel expects at least four K-tiles.");
  static_assert((FixedKTiles % 2) == 0, "Pairwise peeled fixed-shape kernel expects an even K-tile count.");
  static_assert(FixedKTiles * kWmmaK == kFixedBenchmarkK,
                "Fixed-shape peeled kernel must match the benchmark K dimension.");
  static_assert(TileConfig::kTensorBlockN == TensorCoreTile384::kTensorBlockN,
                "The PTX hot-band branch is only expected for the fixed 64x384 kernel.");
  __shared__ __align__(16) __nv_bfloat16 a_shared[2][TileConfig::kASharedTileElems];
  __shared__ __align__(16) __nv_bfloat16 b_shared[2][TileConfig::kBSharedTileElems];
  __shared__ __align__(16)
      float c_shared[TileConfig::kCSharedStageCount * TileConfig::kWarpsPerBlock *
                     TileConfig::kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= TileConfig::kWarpsPerBlock) {
    return;
  }

  const int block_row = (blockIdx.y + block_row_tile_base) * TileConfig::kTensorBlockM;
  const int block_col = blockIdx.x * TileConfig::kTensorBlockN;
  const int warp_tile_m = warp_id / TileConfig::kWarpTilesN;
  const int warp_tile_n = warp_id % TileConfig::kWarpTilesN;
  const int row = block_row + warp_tile_m * kWmmaM;
  const int col = block_col + warp_tile_n * TileConfig::kWarpMmaTilesN * kWmmaN;

  PtxWmmaAccTileSet384 acc_tiles;
  ptx_wmma_fill_zero_tile_set(acc_tiles);

  const __nv_bfloat16* a_block = a + block_row * kFixedBenchmarkK;
  const __nv_bfloat16* b_block = b + block_col;

  stage_a_shared_tile_async<TileConfig>(a_shared[0], a_block, kFixedBenchmarkK);
  stage_b_shared_tile_async<TileConfig>(b_shared[0], b_block, kFixedBenchmarkN);
  cp_async_commit_group();
  stage_a_shared_tile_async<TileConfig>(a_shared[1], a_block + kWmmaK, kFixedBenchmarkK);
  stage_b_shared_tile_async<TileConfig>(
      b_shared[1],
      b_block + kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();
  cp_async_wait_group_1();
  __syncthreads();

  int curr_stage = 0;
  int next_stage = 1;

  #pragma unroll 1
  for (int tile_idx = 0; tile_idx < FixedKTiles - 2; tile_idx += 2) {
    const int first_future_tile_k = (tile_idx + 2) * kWmmaK;
    const int second_future_tile_k = (tile_idx + 3) * kWmmaK;

    advance_peeled_hot_stage_ptx<TileConfig>(
        acc_tiles,
        a_shared,
        b_shared,
        a_block,
        b_block,
        first_future_tile_k,
        warp_tile_m,
        warp_tile_n,
        curr_stage,
        next_stage);

    advance_peeled_hot_stage_ptx<TileConfig>(
        acc_tiles,
        a_shared,
        b_shared,
        a_block,
        b_block,
        second_future_tile_k,
        warp_tile_m,
        warp_tile_n,
        curr_stage,
        next_stage);
  }

  accumulate_peeled_shared_stage_ptx<TileConfig>(
      acc_tiles, a_shared[curr_stage], b_shared[curr_stage], warp_tile_m, warp_tile_n);

  cp_async_wait_group_0();
  __syncthreads();
  curr_stage = next_stage;

  accumulate_peeled_shared_stage_ptx<TileConfig>(
      acc_tiles, a_shared[curr_stage], b_shared[curr_stage], warp_tile_m, warp_tile_n);

  __nv_bfloat16* c_tile_base = c + row * kFixedBenchmarkN + col;
  if constexpr (TileConfig::kCSharedStageCount == 2) {
    ptx_wmma_store_tile_pairs_384<TileConfig>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  } else {
    ptx_wmma_store_tile_set_384<TileConfig>(
        acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
  }
#else
  (void)a;
  (void)b;
  (void)c;
#endif
}

template <int FixedKTiles>
__global__ void bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  static_assert(FixedKTiles > 1,
                "The 256x128 fixed hot-band kernel expects at least two K-tiles.");
  static_assert(FixedKTiles * kWmmaK == kFixedBenchmarkK,
                "The 256x128 fixed hot-band kernel must match the benchmark K dimension.");
  __shared__ __align__(16)
      __nv_bfloat16 a_shared[2][FixedHotBandTile256x128::kASharedTileElems];
  __shared__ __align__(16)
      __nv_bfloat16 b_shared[2][FixedHotBandTile256x128::kBSharedTileElems];
  __shared__ __align__(16)
      float c_shared[FixedHotBandTile256x128::kCSharedStageCount *
                     FixedHotBandTile256x128::kWarpsPerBlock *
                     FixedHotBandTile256x128::kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= FixedHotBandTile256x128::kWarpsPerBlock) {
    return;
  }

  const int block_row = blockIdx.y * FixedHotBandTile256x128::kTensorBlockM;
  const int block_col = blockIdx.x * FixedHotBandTile256x128::kTensorBlockN;
  const int warp_tile_m = warp_id / FixedHotBandTile256x128::kWarpTilesN;
  const int warp_tile_n = warp_id % FixedHotBandTile256x128::kWarpTilesN;
  const int row = block_row + warp_tile_m * FixedHotBandTile256x128::kWarpTileM;
  const int col = block_col + warp_tile_n * FixedHotBandTile256x128::kWarpTileN;

  PtxWmmaAccTileSet64x64 acc_tiles;
  ptx_wmma_fill_zero_tile_set(acc_tiles);

  const __nv_bfloat16* a_block = a + block_row * kFixedBenchmarkK;
  const __nv_bfloat16* b_block = b + block_col;

  stage_a_shared_tile_async<FixedHotBandTile256x128>(
      a_shared[0], a_block, kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile256x128>(
      b_shared[0], b_block, kFixedBenchmarkN);
  cp_async_commit_group();
  stage_a_shared_tile_async<FixedHotBandTile256x128>(
      a_shared[1], a_block + kWmmaK, kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile256x128>(
      b_shared[1],
      b_block + kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();
  cp_async_wait_group_1();
  __syncthreads();

  #pragma unroll 1
  for (int tile_idx = 0; tile_idx < FixedKTiles; ++tile_idx) {
    const int curr_stage = tile_idx & 1;
    const int next_tile_idx = tile_idx + 1;
    const int future_tile_idx = tile_idx + 2;

    const __nv_bfloat16* a_tile =
        a_shared[curr_stage] +
        warp_tile_m * FixedHotBandTile256x128::kWarpTileM * kWmmaK;
    const __nv_bfloat16* b_tile =
        b_shared[curr_stage] +
        b_shared_col_from_logical<FixedHotBandTile256x128>(
            warp_tile_n * FixedHotBandTile256x128::kWarpGroupCols);

    ptx_wmma_accumulate_tile_set_64x64(acc_tiles, a_tile, b_tile);
    // Keep the double-buffered stage live until every warp finishes consuming it.
    __syncthreads();

    if (future_tile_idx < FixedKTiles) {
      const int future_tile_k = future_tile_idx * kWmmaK;
      stage_a_shared_tile_async<FixedHotBandTile256x128>(
          a_shared[curr_stage],
          a_block + future_tile_k,
          kFixedBenchmarkK);
      stage_b_shared_tile_async<FixedHotBandTile256x128>(
          b_shared[curr_stage],
          b_block + future_tile_k * kFixedBenchmarkN,
          kFixedBenchmarkN);
      cp_async_commit_group();
    }

    if (next_tile_idx < FixedKTiles) {
      if (future_tile_idx < FixedKTiles) {
        cp_async_wait_group_1();
      } else {
        cp_async_wait_group_0();
      }
      __syncthreads();
    }
  }

  __nv_bfloat16* c_tile_base = c + row * kFixedBenchmarkN + col;
  ptx_wmma_store_tile_pairs_64x64<FixedHotBandTile256x128>(
      acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
#else
  (void)a;
  (void)b;
  (void)c;
#endif
}

template <int FixedKStages>
__global__ __launch_bounds__(128, 2)
void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  static_assert(FixedKStages > 1,
                "The 128x128x32 fixed hot-band kernel expects at least two K32 stages.");
  static_assert(FixedKStages * kHotBandStageKTiles == kFixedBenchmarkKTiles,
                "The 128x128x32 fixed hot-band kernel must match the benchmark K dimension.");
  __shared__ __align__(16)
      __nv_bfloat16
          a_shared[2][kHotBandStageKTiles * FixedHotBandTile128x128::kASharedTileElems];
  __shared__ __align__(16)
      __nv_bfloat16
          b_shared[2][kHotBandStageKTiles * FixedHotBandTile128x128::kBSharedTileElems];
  __shared__ __align__(16)
      float c_shared[FixedHotBandTile128x128::kCSharedStageCount *
                     FixedHotBandTile128x128::kWarpsPerBlock *
                     FixedHotBandTile128x128::kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= FixedHotBandTile128x128::kWarpsPerBlock) {
    return;
  }

  const int hot_band_tiles_m = kFixedPivotHotRows / FixedHotBandTile128x128::kTensorBlockM;
  const int hot_band_tiles_n = kFixedHotBandN / FixedHotBandTile128x128::kTensorBlockN;
  const int physical_pid = blockIdx.y * hot_band_tiles_n + blockIdx.x;
  const int pids_per_group = kFixedHotBandGroupedRows * hot_band_tiles_n;
  const int group_id = physical_pid / pids_per_group;
  const int first_block_y = group_id * kFixedHotBandGroupedRows;
  const int group_size_y =
      (first_block_y + kFixedHotBandGroupedRows <= hot_band_tiles_m)
          ? kFixedHotBandGroupedRows
          : (hot_band_tiles_m - first_block_y);
  const int pid_in_group = physical_pid % pids_per_group;
  const int logical_block_y = first_block_y + (pid_in_group % group_size_y);
  const int logical_block_x = pid_in_group / group_size_y;

  const int block_row = logical_block_y * FixedHotBandTile128x128::kTensorBlockM;
  const int block_col = logical_block_x * FixedHotBandTile128x128::kTensorBlockN;
  const int warp_tile_m = warp_id / FixedHotBandTile128x128::kWarpTilesN;
  const int warp_tile_n = warp_id % FixedHotBandTile128x128::kWarpTilesN;
  const int row = block_row + warp_tile_m * FixedHotBandTile128x128::kWarpTileM;
  const int col = block_col + warp_tile_n * FixedHotBandTile128x128::kWarpTileN;

  PtxWmmaAccTileSet64x64 acc_tiles;
  ptx_wmma_fill_zero_tile_set(acc_tiles);

  const __nv_bfloat16* a_block = a + block_row * kFixedBenchmarkK;
  const __nv_bfloat16* b_block = b + block_col;

  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[0], a_block, kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[0], b_block, kFixedBenchmarkN);
  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[0] + FixedHotBandTile128x128::kASharedTileElems,
      a_block + kWmmaK,
      kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[0] + FixedHotBandTile128x128::kBSharedTileElems,
      b_block + kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();

  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[1],
      a_block + kHotBandStageKTiles * kWmmaK,
      kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[1],
      b_block + kHotBandStageKTiles * kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[1] + FixedHotBandTile128x128::kASharedTileElems,
      a_block + (kHotBandStageKTiles + 1) * kWmmaK,
      kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[1] + FixedHotBandTile128x128::kBSharedTileElems,
      b_block + (kHotBandStageKTiles + 1) * kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();
  cp_async_wait_group_1();
  __syncthreads();

  #pragma unroll 1
  for (int stage_idx = 0; stage_idx < FixedKStages; ++stage_idx) {
    const int curr_stage = stage_idx & 1;
    const int next_stage_idx = stage_idx + 1;
    const int future_stage_idx = stage_idx + 2;

    const __nv_bfloat16* a_tile_0 =
        a_shared[curr_stage] +
        warp_tile_m * FixedHotBandTile128x128::kWarpTileM * kWmmaK;
    const __nv_bfloat16* a_tile_1 =
        a_shared[curr_stage] + FixedHotBandTile128x128::kASharedTileElems +
        warp_tile_m * FixedHotBandTile128x128::kWarpTileM * kWmmaK;
    const __nv_bfloat16* b_tile_0 =
        b_shared[curr_stage] +
        b_shared_col_from_logical<FixedHotBandTile128x128>(
            warp_tile_n * FixedHotBandTile128x128::kWarpGroupCols);
    const __nv_bfloat16* b_tile_1 =
        b_shared[curr_stage] + FixedHotBandTile128x128::kBSharedTileElems +
        b_shared_col_from_logical<FixedHotBandTile128x128>(
            warp_tile_n * FixedHotBandTile128x128::kWarpGroupCols);

    ptx_wmma_accumulate_tile_set_64x64(acc_tiles, a_tile_0, b_tile_0);
    ptx_wmma_accumulate_tile_set_64x64(acc_tiles, a_tile_1, b_tile_1);
    // Keep the two-K-tile stage live until every warp finishes consuming both halves.
    __syncthreads();

    if (future_stage_idx < FixedKStages) {
      const int future_tile_k = future_stage_idx * kHotBandStageKTiles * kWmmaK;
      stage_a_shared_tile_async<FixedHotBandTile128x128>(
          a_shared[curr_stage],
          a_block + future_tile_k,
          kFixedBenchmarkK);
      stage_b_shared_tile_async<FixedHotBandTile128x128>(
          b_shared[curr_stage],
          b_block + future_tile_k * kFixedBenchmarkN,
          kFixedBenchmarkN);
      stage_a_shared_tile_async<FixedHotBandTile128x128>(
          a_shared[curr_stage] + FixedHotBandTile128x128::kASharedTileElems,
          a_block + future_tile_k + kWmmaK,
          kFixedBenchmarkK);
      stage_b_shared_tile_async<FixedHotBandTile128x128>(
          b_shared[curr_stage] + FixedHotBandTile128x128::kBSharedTileElems,
          b_block + (future_tile_k + kWmmaK) * kFixedBenchmarkN,
          kFixedBenchmarkN);
      cp_async_commit_group();
    }

    if (next_stage_idx < FixedKStages) {
      if (future_stage_idx < FixedKStages) {
        cp_async_wait_group_1();
      } else {
        cp_async_wait_group_0();
      }
      __syncthreads();
    }
  }

  __nv_bfloat16* c_tile_base = c + row * kFixedBenchmarkN + col;
  ptx_wmma_store_tile_pairs_64x64<FixedHotBandTile128x128>(
      acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
#else
  (void)a;
  (void)b;
  (void)c;
#endif
}

template <int FixedKTiles>
__global__ __launch_bounds__(128, 2)
void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  static_assert(FixedKTiles > 1,
                "The 128x128 fixed hot-band kernel expects at least two K-tiles.");
  static_assert(FixedKTiles * kWmmaK == kFixedBenchmarkK,
                "The 128x128 fixed hot-band kernel must match the benchmark K dimension.");
  __shared__ __align__(16)
      __nv_bfloat16 a_shared[2][FixedHotBandTile128x128::kASharedTileElems];
  __shared__ __align__(16)
      __nv_bfloat16 b_shared[2][FixedHotBandTile128x128::kBSharedTileElems];
  __shared__ __align__(16)
      float c_shared[FixedHotBandTile128x128::kCSharedStageCount *
                     FixedHotBandTile128x128::kWarpsPerBlock *
                     FixedHotBandTile128x128::kCSharedTileElemsPerWarp];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= FixedHotBandTile128x128::kWarpsPerBlock) {
    return;
  }

  const int block_row = blockIdx.y * FixedHotBandTile128x128::kTensorBlockM;
  const int block_col = blockIdx.x * FixedHotBandTile128x128::kTensorBlockN;
  const int warp_tile_m = warp_id / FixedHotBandTile128x128::kWarpTilesN;
  const int warp_tile_n = warp_id % FixedHotBandTile128x128::kWarpTilesN;
  const int row = block_row + warp_tile_m * FixedHotBandTile128x128::kWarpTileM;
  const int col = block_col + warp_tile_n * FixedHotBandTile128x128::kWarpTileN;

  PtxWmmaAccTileSet64x64 acc_tiles;
  ptx_wmma_fill_zero_tile_set(acc_tiles);

  const __nv_bfloat16* a_block = a + block_row * kFixedBenchmarkK;
  const __nv_bfloat16* b_block = b + block_col;

  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[0], a_block, kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[0], b_block, kFixedBenchmarkN);
  cp_async_commit_group();
  stage_a_shared_tile_async<FixedHotBandTile128x128>(
      a_shared[1], a_block + kWmmaK, kFixedBenchmarkK);
  stage_b_shared_tile_async<FixedHotBandTile128x128>(
      b_shared[1],
      b_block + kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();
  cp_async_wait_group_1();
  __syncthreads();

  #pragma unroll 2
  for (int tile_idx = 0; tile_idx < FixedKTiles; ++tile_idx) {
    const int curr_stage = tile_idx & 1;
    const int next_tile_idx = tile_idx + 1;
    const int future_tile_idx = tile_idx + 2;

    const __nv_bfloat16* a_tile =
        a_shared[curr_stage] +
        warp_tile_m * FixedHotBandTile128x128::kWarpTileM * kWmmaK;
    const __nv_bfloat16* b_tile =
        b_shared[curr_stage] +
        b_shared_col_from_logical<FixedHotBandTile128x128>(
            warp_tile_n * FixedHotBandTile128x128::kWarpGroupCols);

    ptx_wmma_accumulate_tile_set_64x64(acc_tiles, a_tile, b_tile);

    if (future_tile_idx < FixedKTiles) {
      // Keep the double-buffered stage live until every warp finishes consuming it.
      __syncthreads();
      const int future_tile_k = future_tile_idx * kWmmaK;
      stage_a_shared_tile_async<FixedHotBandTile128x128>(
          a_shared[curr_stage],
          a_block + future_tile_k,
          kFixedBenchmarkK);
      stage_b_shared_tile_async<FixedHotBandTile128x128>(
          b_shared[curr_stage],
          b_block + future_tile_k * kFixedBenchmarkN,
          kFixedBenchmarkN);
      cp_async_commit_group();
    }

    if (next_tile_idx < FixedKTiles) {
      if (future_tile_idx < FixedKTiles) {
        cp_async_wait_group_1();
      } else {
        cp_async_wait_group_0();
      }
      __syncthreads();
    }
  }

  __nv_bfloat16* c_tile_base = c + row * kFixedBenchmarkN + col;
  ptx_wmma_store_tile_pairs_64x64<FixedHotBandTile128x128>(
      acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
#else
  (void)a;
  (void)b;
  (void)c;
#endif
}

template <int FixedKTiles>
__global__ __launch_bounds__(128, 2)
void bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel(
    const __nv_bfloat16* a,
    const __nv_bfloat16* b,
    __nv_bfloat16* c) {
#if defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 800
  static_assert(FixedKTiles > 1,
                "The 128x128 PTX microkernel branch expects at least two K-tiles.");
  static_assert(FixedKTiles * kWmmaK == kFixedBenchmarkK,
                "The 128x128 PTX microkernel branch must match the benchmark K dimension.");
  __shared__ __align__(16)
      __nv_bfloat16 a_shared[2][FixedHotBandTile128x128::kASharedTileElems];
  __shared__ __align__(16)
      __nv_bfloat16 b_shared[2][FixedHotBandTile128x128::kBSharedTileElems];
  __shared__ __align__(16)
      float c_shared[FixedHotBandTile128x128PtxExportScratch::kTotalElems];

  const int warp_id = threadIdx.x / kWarpSize;
  const int lane_id = threadIdx.x % kWarpSize;

  if (warp_id >= FixedHotBandTile128x128::kWarpsPerBlock) {
    return;
  }

  const int block_row = blockIdx.y * FixedHotBandTile128x128::kTensorBlockM;
  const int block_col = blockIdx.x * FixedHotBandTile128x128::kTensorBlockN;
  const int warp_tile_m = warp_id / FixedHotBandTile128x128::kWarpTilesN;
  const int warp_tile_n = warp_id % FixedHotBandTile128x128::kWarpTilesN;
  const int row = block_row + warp_tile_m * FixedHotBandTile128x128::kWarpTileM;
  const int col = block_col + warp_tile_n * FixedHotBandTile128x128::kWarpTileN;

  PtxWmmaAccTileSet64x64 acc_tiles;
  ptx_wmma_fill_zero_tile_set(acc_tiles);

  const __nv_bfloat16* a_block = a + block_row * kFixedBenchmarkK;
  const __nv_bfloat16* b_block = b + block_col;

  stage_a_shared_tile_async_ptx_microkernel(
      a_shared[0], a_block, kFixedBenchmarkK);
  stage_b_shared_tile_async_ptx_microkernel(
      b_shared[0], b_block, kFixedBenchmarkN);
  cp_async_commit_group();
  stage_a_shared_tile_async_ptx_microkernel(
      a_shared[1], a_block + kWmmaK, kFixedBenchmarkK);
  stage_b_shared_tile_async_ptx_microkernel(
      b_shared[1],
      b_block + kWmmaK * kFixedBenchmarkN,
      kFixedBenchmarkN);
  cp_async_commit_group();
  cp_async_wait_group_1();
  __syncthreads();

  #pragma unroll 2
  for (int tile_idx = 0; tile_idx < FixedKTiles; ++tile_idx) {
    const int curr_stage = tile_idx & 1;
    const int next_tile_idx = tile_idx + 1;
    const int future_tile_idx = tile_idx + 2;

    const __nv_bfloat16* a_tile =
        a_shared[curr_stage] +
        warp_tile_m * FixedHotBandTile128x128::kWarpTileM * kWmmaK;
    const __nv_bfloat16* b_tile =
        b_shared[curr_stage] +
        b_shared_col_from_logical<FixedHotBandTile128x128>(
            warp_tile_n * FixedHotBandTile128x128::kWarpGroupCols);

    ptx_wmma_accumulate_tile_set_64x64_ptx_microkernel(
        acc_tiles, a_tile, b_tile);

    if (future_tile_idx < FixedKTiles) {
      // Keep the restored accepted base intact while isolating future PTX work
      // to this active hot-band branch symbol.
      __syncthreads();
      const int future_tile_k = future_tile_idx * kWmmaK;
      stage_a_shared_tile_async_ptx_microkernel(
          a_shared[curr_stage],
          a_block + future_tile_k,
          kFixedBenchmarkK);
      stage_b_shared_tile_async_ptx_microkernel(
          b_shared[curr_stage],
          b_block + future_tile_k * kFixedBenchmarkN,
          kFixedBenchmarkN);
      cp_async_commit_group();
    }

    if (next_tile_idx < FixedKTiles) {
      if (future_tile_idx < FixedKTiles) {
        cp_async_wait_group_1();
      } else {
        cp_async_wait_group_0();
      }
      __syncthreads();
    }
  }

  __nv_bfloat16* c_tile_base = c + row * kFixedBenchmarkN + col;
  ptx_wmma_store_tile_pairs_64x64_ptx_microkernel(
      acc_tiles, c_shared, c_tile_base, warp_id, lane_id);
#else
  (void)a;
  (void)b;
  (void)c;
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
      bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<
          kFixedBenchmarkKTiles><<<
              dim3(kFixedHotBandN / FixedHotBandTile128x128::kTensorBlockN,
                   kFixedPivotHotRows / FixedHotBandTile128x128::kTensorBlockM,
                   1),
              dim3(FixedHotBandTile128x128::kWarpsPerBlock * kWarpSize, 1, 1),
              0,
              stream>>>(a, b, c);

      launch_fixed_peeled_hot_band_row_band<
          TensorCoreTile384,
          kFixedBenchmarkKTiles>(
              a,
              b,
              c,
              kFixedPivotHotRows / TensorCoreTile384::kTensorBlockM,
              kFixedResidualHotRows / TensorCoreTile384::kTensorBlockM,
              stream);

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
