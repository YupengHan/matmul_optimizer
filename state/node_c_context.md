# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim the hot-band export path by batching 64x64 stores vertically instead of horizontally`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_223457`
- round loop: `round 1/50`
- hypothesis: `The dominant hot-band kernel is back on the best known surface and recent copy / consumer experiments have mostly been negative. The current 64x64 export helper still pays one `__syncwarp()` per row and per column pair, which means eight warp synchronizations to export the sixteen 16x16 accumulator tiles. Because each warp only has two `c_shared` scratch stages, a practical next move is to flip the batching dimension: use those two stages to store two rows for the same column tile, then export them together. That preserves shared footprint and accumulator layout while potentially cutting the export-side warp sync count in half.`
- expected bottleneck: `Hot-band epilogue / export synchronization and shared-memory round-trip overhead.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_export_shared_tile_quads_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x64`
- risk: `Moderate. The change is local and footprint-neutral, but the export path is correctness-sensitive and the accumulator-to-output mapping must stay exact.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread`

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
