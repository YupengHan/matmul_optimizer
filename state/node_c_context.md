# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea two-level B staging follow-through: footprint-neutral B shared permutation on top of the current streaming consumer path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_213703`
- round loop: `round 9/10`
- hypothesis: `Round 8 suggests the B-feed family is finally moving the right metrics without raising registers or shared memory, but issue-order alone is not enough. The next step is the user's earlier producer-layout / consumer-layout split, done inside the existing footprint: keep the current single-fragment mirrored consumer path, but change the physical placement of B chunks in shared memory so `stage_b_shared_tile_async` writes a bank-friendlier order and `b_shared_col_from_logical` maps logical consumer columns back onto that permuted layout. This keeps macro tiling, stage depth, and cp.async volume fixed while making the producer and consumer views of B deliberately different.`
- expected bottleneck: `Warp-local shared/L1 operand delivery and bank behavior on the hot-band B fragment path rather than CTA-level control flow.`
- code locations: `src/kernels/bf16_gemm_v1.cu:b_shared_col_from_logical, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_b_row, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_tiles_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Moderate. This is still correctness-sensitive, and the shared permutation has to preserve 16-byte async-copy alignment plus the current footprint. The guardrail is strict: no second B shared tile, no CTA repack, no extra barrier, no stage-depth loss.`
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
