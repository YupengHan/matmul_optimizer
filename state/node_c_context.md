# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea bank conflict: reverse the mirrored 64x64 B sweep into a `Right Left Right Left` order`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_221629`
- round loop: `round 7/30`
- hypothesis: `The current hot-band PTX path is still living on the B-consumer improvements: it keeps `mio_throttle` low, but short scoreboard is still about 6.77 and tensor active is still stuck around 38.57% with one-CTA occupancy. The user specifically asked to keep future bank-conflict work warp-local and avoid any extra shared-memory footprint. The cleanest next experiment is therefore to keep the same shared layout, same stage depth, and same one-fragment B lookahead, but replace the current edge-in mirrored order with the opposite `Right Left Right Left` sweep so the warp touches the right-most column tile first and alternates back across the 64x64 micro-tile.`
- expected bottleneck: `Residual warp-local B delivery / bank behavior inside the 64x64 hot-band consumer path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:PtxWmmaMirroredTileIndex64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_col_fragment_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_tiles_64x64`
- risk: `Moderate. The change is local and respects the no-extra-shared rule, but the current sweep is already measured and a different order can easily regress feed behavior.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread`

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
