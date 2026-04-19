# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore explicit cp.async warm-up and consume ordering`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_212050`
- round loop: `round 3/5`
- hypothesis: `Treat the wait-group reorder in `deeb976` as the primary regression source. The previous measured kernel `aee3c09` was 3/3 correct at 101.375 ms, while the new version removed the initial `cp_async_wait_group_0()` plus `__syncthreads()` before the first consume and now issues next-stage copies before the current stage is proven visible. With all 3 correctness cases now failing and runtime slightly worse, the best next step is to reintroduce a distinct warm-up, steady-state, and drain sequence so `wmma::load_matrix_sync` never reads a stage that is still in-flight.`
- expected bottleneck: `Correctness-breaking cp.async producer/consumer hazard in the ping-pong pipeline; after recovery, the remaining limit is still CTA synchronization and MIO throttle rather than DRAM saturation.`
- code locations: `src/kernels/bf16_gemm_v1.cu:50-59, src/kernels/bf16_gemm_v1.cu:151-173, src/kernels/bf16_gemm_v1.cu:175-180`
- risk: `Low to moderate. This is the most targeted fix and should recover correctness fastest, but if the repaired schedule becomes too conservative it may give back the small long-scoreboard improvement without reducing barrier pressure.`
- metrics to re-check: `correctness cases 3/3, median runtime vs 101.3749619 ms from aee3c09, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
