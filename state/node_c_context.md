# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reduce hot-kernel epilogue and writeback work on the accepted 64x384 base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_014602`
- round loop: `round 20/20`
- hypothesis: `The accepted round-18 result already proved that 64x384 over the first 7680 columns plus the 64x96 tail is the right macro split on this NVIDIA GeForce RTX 3070 Laptop GPU (sm86). The next gain should come from instruction-mix cleanup, not another feed-path rewrite: on the accepted round-18 base the main 64x384 kernel still spent 77.865532% of issue on LSU instructions, stalled 31.42% on MIO throttle, and only reached 32.130750% tensor active. Every warp currently stores each 16x16 accumulator tile through shared float scratch, does two __syncwarp calls per tile, then runs a lane-strided BF16 pack/store loop. That non-tensor writeback path was not the target of round 19 and is a better next lever than the regressed B-layout family.`
- expected bottleneck: `Non-tensor epilogue work and shared-scratch writeback are diluting Tensor Core issue inside the proven 64x384 hot kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:189-192 (round-18 base ea27d5a, BF16 pair packing helper), src/kernels/bf16_gemm_v1.cu:374-376 (round-18 base ea27d5a, c_shared scratch allocation), src/kernels/bf16_gemm_v1.cu:440-462 (round-18 base ea27d5a, WMMA store and epilogue writeback loop)`
- risk: `Moderate. The edit surface is localized and avoids the round-19 regression family, but WMMA accumulator export paths are awkward and a bad rewrite can just trade one LSU pattern for another or break BF16 packing correctness.`
- metrics to re-check: `main-kernel sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, main-kernel sm__inst_executed.avg.pct_of_peak_sustained_elapsed, main-kernel smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, main-kernel sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, main-kernel smsp__warp_issue_stalled_barrier_per_warp_active.pct, median_runtime_ms`

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
