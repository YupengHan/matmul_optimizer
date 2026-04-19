# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep 64x384, but rework the hot-kernel shared/L1 feed path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_013222`
- round loop: `round 19/20`
- hypothesis: `Round 18 autotune is strong evidence that the correct macro choice on this RTX 3070 Laptop GPU (sm86) is 64x384 over the first 7680 columns plus the 64x96 tail; node_a already validated that path at 38.47372818 ms. The remaining gap is inside the 64x384 hot kernel itself: raw NCU details show 126 registers/thread, 38.4 KB shared/block, 77.865532% LSU instruction issue, 48.590499% LSU wavefront activity, 31.42% MIO throttle, and only 32.130750% tensor active. The current B staging scheme only inserts a coarse 16-byte skew between warp groups, so a stronger B-tile swizzle/padding layout and corresponding load-path cleanup should let the same 64x384 CTA spend fewer cycles servicing shared/L1 traffic and more cycles issuing Tensor Core MMA.`
- expected bottleneck: `Shared-memory and LSU feed pressure in the 64x384 hot band is throttling Tensor Core issue; the problem is now on-chip instruction mix and staging efficiency, not the macro tile width.`
- code locations: `src/kernels/bf16_gemm_v1.cu:195-225, src/kernels/bf16_gemm_v1.cu:374-375, src/kernels/bf16_gemm_v1.cu:423-431`
- risk: `Moderate. Shared-layout and fragment-load changes are localized to the hot path and fit the autotune evidence, but a bad swizzle can silently hurt correctness or just move pressure around without lowering MIO throttle.`
- metrics to re-check: `main-kernel smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, main-kernel l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, main-kernel l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, main-kernel sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, main-kernel sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, median_runtime_ms`

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
