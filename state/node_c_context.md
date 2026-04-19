# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Main-kernel producer/consumer cp.async pipeline`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_235617`
- round loop: `round 11/20`
- hypothesis: `Using the heuristics' copy-pipeline and register-pressure lenses, the round-10 main/tail split appears to have already bought the easy barrier win, but the hot 64x128 main kernel is now dominated by feed-side instruction pressure: the main kernel carries essentially all runtime, sits at 55 registers/thread with a 4-block register limit, and shows 41.76% MIO throttle with L1TEX/LSU request rates near 82.8%. Converting the current all-warps-do-copy ping-pong into a producer/consumer cp.async pipeline for the 64x128 path should move copy issue pressure off the MMA warps, keep the larger math-per-barrier shape, and raise tensor activity without giving back the round-10 gain.`
- expected bottleneck: `Main-path MIO/LSU issue saturation in the 64x128 feed pipeline, with residual CTA-wide handoff cost as a secondary limiter.`
- code locations: `src/kernels/bf16_gemm_v1.cu:27-48 (TileConfig staging geometry, warp-group sizing, and async-copy work split), src/kernels/bf16_gemm_v1.cu:111-137 (stage_a_shared_tile_async and stage_b_shared_tile_async), src/kernels/bf16_gemm_v1.cu:191-255 (current all-warps cp.async preload, ping-pong loop, and CTA-wide waits)`
- risk: `High: on Ampere, a producer/consumer pipeline can easily underfill Tensor Cores if too many warps become loaders, and the extra staging state may further raise registers or shared memory before it helps.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, launch__registers_per_thread, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed`

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
