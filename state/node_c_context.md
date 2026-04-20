# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea bank conflict: increase the hot-band B shared-memory padding from +8 to +16 elements`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_223724`
- round loop: `round 2/50`
- hypothesis: `The vertical export rewrite was effectively neutral on the dominant kernel, which means the next clean experiment should stay on the operand-delivery side. The hot-band path still uses WMMA-style shared loads for B and currently inserts only one 16-byte skew between the two 64-column warp groups. A slightly larger padding offset can change how the second half of the 128-column shared tile maps into banks without changing tile shape, consumer order, or stage count. Because the hot-band shared footprint still has headroom under the 48 KiB budget, this is a controlled bank-conflict test.`
- expected bottleneck: `Residual B-side shared-memory bank behavior in the hot-band WMMA/PTX consumer path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile256x128::kBSharedStride, src/kernels/bf16_gemm_v1.cu:b_shared_col_from_logical, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async`
- risk: `Low to moderate. The change is very small and local, but it does increase shared-memory footprint slightly and may do nothing if the existing skew is already sufficient.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
