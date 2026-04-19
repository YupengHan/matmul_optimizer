# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_02`
- direction name: `Retile CTA and warp partition to trim per-warp N baggage`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_004022`
- round loop: `round 15/20`
- hypothesis: `The current 4x2 warp layout with a wide per-warp N fanout keeps the accepted main/tail split, but each warp still carries multiple N fragments and a relatively heavy B-side footprint. Retiling the CTA or warp work split to reduce per-warp N baggage should ease fragment handling and MIO pressure without abandoning the proven split between the 64x128 main path and the 64x96 tail path.`
- expected bottleneck: `Per-warp fragment baggage and B-side staging pressure caused by the current CTA/warp partition, reflected in MIO throttle and possibly excess register footprint from carrying multiple N-side fragments per warp.`
- code locations: `src/kernels/bf16_gemm_v1.cu: kTensorWarpTilesM, kTensorWarpTilesN, and TensorCoreTileConfig warp/CTA shape constants, src/kernels/bf16_gemm_v1.cu: TensorCoreTile96 and TensorCoreTile128 specializations plus derived kWarpGroupCols and kTensorBlockN values, src/kernels/bf16_gemm_v1.cu: fixed-shape main/tail launch geometry in launch_bf16_gemm_v1`
- risk: `Medium risk. A narrower per-warp N assignment can reduce fragment baggage, but it may also weaken reuse, increase CTA count, or create a worse balance between tensor utilization and memory traffic if the new partition is too fine-grained.`
- metrics to re-check: `median runtime, TFLOP/s, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
