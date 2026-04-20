# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea bank-conflict follow-through: warp-local B consumer transform on the restored accepted base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_213118`
- round loop: `round 8/10`
- hypothesis: `Round 7 falsified the current L2/block-order clue, and round 6 already falsified the pure fixed-shape Stage rewrite. That leaves the current wall where the earlier diagnoses kept pointing: operand feed on the correct hot-band kernel. The implementation surface has now been restored to the accepted base, so the next move is to keep the same 64x384 outer shape, the same shared footprint, and the same stage depth, but retune only the warp-local B consumer path in the 64x64 PTX micro-tile. The key is to do something stronger than the earlier simple mirrored pair order: for example a lane-aware pair permutation or a shared-address permutation that changes how each warp consumes B fragments without reintroducing CTA repack or a second shared tile.`
- expected bottleneck: `Warp-local shared/L1 operand delivery and bank behavior on B fragment loads in the true hot-band kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_b_row, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:b_shared_col_from_logical`
- risk: `Moderate. This family is correctness-sensitive, and one earlier order-only variant had low signal, so the next attempt has to be more structural than a cosmetic reorder while still preserving the current shared/register budgets.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, launch__shared_mem_per_block_allocated`

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
