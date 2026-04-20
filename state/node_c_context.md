# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen PTX Prefetch Handoff On Top Of The New Export Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_160829`
- round loop: `round 9/17`
- hypothesis: `Round 8/17 closed the deeper row-pair export cleanup, but round 7/17 established a much better accepted base at 24.84582424 ms by simplifying the PTX export helper. That materially changes the ranking of the remaining families. The earlier prefetch-handoff experiment was negative on the older base, but it also drove long-scoreboard down much harder than the grouping-window attempt. Now that export overhead has been reduced, the next best move is to re-open the PTX prefetch family with a narrower retime on top of the new accepted export base instead of digging deeper into export cleanup again.`
- expected bottleneck: `Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1994-2006, src/kernels/bf16_gemm_v1.cu:2027-2039`
- risk: `Medium. The family already had one losing attempt, so this should be a narrower retime than round 4/17, but it now sits on a cleaner export baseline that may change the tradeoff.`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
