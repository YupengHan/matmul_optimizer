# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the restored correct surface and let only half the CTA issue hot-band Pg2s async copies`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_231228`
- round loop: `round 11/50`
- hypothesis: `The light L2 swizzle was basically flat, which leaves the user's Pg2s/staging idea as the next low-risk family. The current hot-band kernel still has all 256 threads participate in both A and B staging, even though tensor activity remains around 38.6% and the main kernel is not obviously DRAM bound. A conservative first step is to keep the tile shape and consumer math unchanged but have only the first 128 threads issue the cp.async staging loops for the hot-band kernel. That tests whether reducing staging-side scheduler pressure helps without taking the correctness risks of a true producer-only warp split.`
- expected bottleneck: `CTA-level staging orchestration and LSU/shared issue pressure during Pg2s rather than warp-local MMA scheduling.`
- code locations: `src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Moderate. The copy count stays identical, but a poorer producer subset could just add loop overhead without reducing the real bottleneck.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
