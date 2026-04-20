# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Repair the A-side lookahead as an explicit fixed-shape row-pair preload, then revalidate correctness`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_220618`
- round loop: `round 4/30`
- hypothesis: `This run is not acceptable as-is because correctness failed on all three cases, but it is still informative: runtime improved from 30.592960 ms to 30.270464 ms and the hot-band kernel shortened from about 41.19 us to about 40.99 us. That combination suggests the A-side Ps2r idea may be directionally right while the recursive row-pair implementation is wrong. The best next move is therefore not to throw the family away immediately, but to rewrite the row-pair lookahead into a flatter fixed-shape sequence that preloads the second row-pair explicitly, removes the recursive fragment handoff, and checks whether the performance signal survives once correctness is restored.`
- expected bottleneck: `Implementation / codegen risk in the current A-side lookahead path, plus residual shared-to-register A-feed latency if the idea survives repair.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_row_pair_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64_lookahead, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64`
- risk: `Moderate. The rewrite is local and directly motivated by a real speed signal, but if correctness is restored only by undoing the additional overlap, the family may collapse back to the round-2 baseline.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
