# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea register reuse: phase the 64x64 hot-band warp tile into two 64x32 accumulator panels`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_215936`
- round loop: `round 3/30`
- hypothesis: `The one-fragment B-side Ps2r lookahead preserved the recovered streaming-B gain but only moved runtime from 30.618112 ms to 30.592960 ms because the hot-band kernel is still pinned at 167 registers per thread and one CTA per SM. The next higher-ceiling move is to keep the 256x128 CTA and 64x64 warp footprint but serialize the four warp-local output columns as two mirrored 64x32 panels, so each warp carries roughly half the accumulator live set at once instead of all sixteen 16x16 accumulator fragments. If that drops registers materially, the hot-band path has a chance to recover more active warps and improve tensor issue instead of chasing another tiny feed-side win inside the same occupancy wall.`
- expected bottleneck: `Register-limited occupancy and warp-level live-fragment pressure in the hot-band PTX microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:PtxWmmaAccTileSet64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_tiles_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `High. This changes the hot-band accumulator residency model and may trade register relief for extra export/control overhead. If the panelization forces too much extra store traffic or synchronization, it can lose despite lower registers.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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
