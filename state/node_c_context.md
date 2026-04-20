# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Peel the 452-tile steady state for the shared 64x64 PTX hot-band family`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_224955`
- round loop: `round 4/50`
- hypothesis: `The new residual 64x128 PTX kernel did cut the last-64-row strip from 0.866 ms to 0.702 ms, but the dominant 256x128 hot-band kernel stayed essentially flat at 41.080 ms vs the accepted base's 40.911 ms while tensor activity, barrier stalls, short scoreboard stalls, and registers all stayed nearly unchanged. That points back to the generic tile_idx loop itself: every one of the 452 K-tiles still pays next/future bounds checks, stage-select logic, and cp.async wait branching. Now that both the pivot kernel and the residual kernel share one 64x64 PTX microkernel family, the best next structural move is to split them into fixed-shape prologue / steady-state / epilogue loops and let the compiler see the exact 452-tile schedule.`
- expected bottleneck: `Hot-band control/orchestration overhead inside the fixed-shape PTX main loop, which is still diluting tensor issue after the residual path was specialized.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_64x64_kernel, src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:launch_fixed_hot_band_ptx_region`
- risk: `Moderate. A previous steady-state peeling attempt failed on a different path, so the cp.async commit/wait ordering must stay exact, but the scope is now cleaner because both hot-band kernels share the same PTX microkernel family.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread`

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

- no tracked dirty paths at prepare time
