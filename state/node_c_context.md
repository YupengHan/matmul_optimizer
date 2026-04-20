# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the 26.924 ms K16 base and promote the real 256x128 CTA / 64x64 warp hot-band branch onto the default path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_004413`
- round loop: `round 34/100`
- hypothesis: `Round 33 showed that promoting the active hot-band path to bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel was the wrong use of the human idea families: runtime regressed from the accepted 26.924031 ms base to 31.684608 ms while tensor-active fell from 48.56 to 40.12 and long-scoreboard rose from 1.31 to 6.02. That rejects a deeper Async Copy + Pg2s + Stage rewrite on the active 128x128 path for now. The next real-path move should restore the accepted 128x128 K16 branch around commit 1b9dbe3, then activate the already-written bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel on the default fixed-shape hot band. This is the clearest acceptance of the human Tiling family for this round: 256x128 block tiling with 64x64 warp tiling, while keeping the proven 16-byte cp.async, shared-memory reuse, and two-stage pipeline instead of adding more orchestration.`
- expected bottleneck: `Tensor Core under-utilization caused by the current active hot-band geometry and control path, not by raw DRAM bandwidth. The target is to raise tensor-active and useful work per CTA without reintroducing the K32 feed/orchestration penalties.`
- code locations: `src/kernels/bf16_gemm_v1.cu:80-107 (FixedHotBandTile256x128 and FixedHotBandTile128x128 shape definitions), src/kernels/bf16_gemm_v1.cu:1367-1463 (bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel), src/kernels/bf16_gemm_v1.cu:1620-1712 (accepted 128x128 K16 hot-band kernel to restore as the comparison base), src/kernels/bf16_gemm_v1.cu:1739-1786 (launch_bf16_gemm_v1 default fixed-shape dispatch and hot-band split)`
- risk: `Medium. This is a real active-path change with meaningful upside, but the launch split has to preserve the accepted base behavior outside the promoted pivot hot band. If tensor-active does not recover over the K32 regression, the branch could simply trade one scheduling mismatch for another.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
