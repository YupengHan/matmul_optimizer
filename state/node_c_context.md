# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Split the fixed shape into a 64x128 main kernel plus a 64x96 tail kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_234449`
- round loop: `round 10/20`
- hypothesis: `Using docs/heuristics.md explicitly, the current 64x96 result now reads as a class-1 plus class-5 problem rather than a plain DRAM ceiling: tensor active is only 28.78%, barrier stall is 29.48%, MIO throttle is 34.18%, long scoreboard is just 0.75%, and DRAM is only 47.58%. Because the fixed N dimension is exactly 7776 = 60 * 128 + 96, most CTAs can run a wider 64x128 main path while a separate 64x96 tail kernel handles the remainder. That should make each staged A/B slice pay for four N fragments per warp on 60 of 81 CTAs, materially increasing math per barrier and per fragment-load episode.`
- expected bottleneck: `Barrier and fragment-feed overhead in the steady-state K loop; the current CTA already improved residency, so the next step is to amortize `cp.async`, `__syncthreads()`, and `wmma::load_matrix_sync` across more MMA before the next handoff.`
- code locations: `src/kernels/bf16_gemm_v1.cu:22-57 (tile-shape constants, B-stage footprint, and static guards), src/kernels/bf16_gemm_v1.cu:158-249 (tensor-core kernel warp mapping, K-loop, and MMA/feed structure), src/kernels/bf16_gemm_v1.cu:263-289 (launch dispatch that would need a fixed-shape 64x128 main path plus 64x96 tail split)`
- risk: `Moderate to high. The extra accumulator fragment and wider B slab can push the kernel above the current 48 registers/thread and 19.968 KB/block envelope, and the split launch must keep the 96-column tail path simple enough that the main-path gain is not diluted.`
- metrics to re-check: `median_runtime_ms, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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

- no tracked dirty paths at prepare time
