# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Specialize the fixed-shape K loop so the 4-warp CTA spends less time in barrier and control overhead`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_232136`
- round loop: `round 8/20`
- hypothesis: `The occupancy-neutral B-gap restore already brought the kernel back to the accepted 13.824 KB/block footprint and 58.03% active-warps level, so the residual gap is no longer explained by lost residency. The current profile is instead dominated by per-step control costs inside the tensor mainloop: barrier stall is still 22.82%, MIO throttle is 31.63%, long-scoreboard is only 2.33%, and the detailed CSV still shows 12.00% uniform-pipe issue activity. Because this benchmark shape is exactly divisible by the 32x96x16 tensor tile, the `tile_k` loop can be peeled into prologue, branch-free steady state, and drain so the hot path stops rechecking `next_tile_k < k` and carries less wait/sync bookkeeping around every MMA step.`
- expected bottleneck: `Synchronization and hot-path control overhead in the double-buffered async-copy pipeline`
- code locations: `src/kernels/bf16_gemm_v1.cu:69-78 (`cp_async_commit_group` / `cp_async_wait_group_0` helpers), src/kernels/bf16_gemm_v1.cu:187-225 (pipeline warmup plus the per-K-step wait/sync sequence), src/kernels/bf16_gemm_v1.cu:279-282 (exact-shape tensor launch gate)`
- risk: `Low to moderate. The likely upside is incremental, and changing the steady-state stage ordering can silently break overlap or introduce off-by-one drain bugs even when the fixed shape still passes correctness.`
- metrics to re-check: `median_runtime_ms, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__inst_executed_pipe_uniform.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness_passed`

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
