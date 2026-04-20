# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Finish Flattening PTX Export Across Tile Rows`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_154908`
- round loop: `round 3/17`
- hypothesis: `Round 2/17 validated the PTX export-helper family: runtime improved from 26.978816 ms back down to 25.505328 ms, DRAM stayed anchored near 11.5%, and long-scoreboard dropped from 7.79 to 7.21. The current helper still recurses over `TileRow`, so the next best move is to finish that specialization and make the hot-band export fully explicit across the four tile rows. That keeps the single-stage scratch and recovered locality intact while trimming the remaining recursive control and repeated row-base setup in the epilogue.`
- expected bottleneck: `Residual PTX export-side control overhead and per-row epilogue orchestration inside the hot-band microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:925-947, src/kernels/bf16_gemm_v1.cu:1008-1056, src/kernels/bf16_gemm_v1.cu:2025-2027`
- risk: `Low to medium. This continues the only family with a clean recent win and does not widen scope beyond the existing one-stage PTX export helper, but the remaining upside may now be incremental rather than step-sized.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness`

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
