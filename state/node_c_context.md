# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea stage: restore the pre-sweep best surface and peel the hot-band K loop into steady-state`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_221835`
- round loop: `round 8/30`
- hypothesis: `The reversed B sweep is a clear negative and should not be the surface for further work. The next human-idea direction is therefore to restore the pre-sweep best hot-band consumer order and then specialize the 452-tile hot-band K loop into prologue, steady-state, and epilogue so the common path no longer pays `future_tile_idx` / `next_tile_idx` branch logic every iteration. Because the hot-band kernel is already fully fixed-shape and uses `#pragma unroll 1`, this is the cleanest remaining control-side experiment on top of the best-known warp-local consumer path.`
- expected bottleneck: `Fixed-shape control-flow and stage-transition overhead inside the hot-band K loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:PtxWmmaMirroredTileIndex64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Moderate. The idea is mechanically straightforward, but the hot-band pipeline is delicate and the specialization must preserve the proven pre-sweep consumer order while removing only the generic loop branches.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread`

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
