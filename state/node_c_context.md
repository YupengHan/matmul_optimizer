# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune PTX Prefetch Handoff On Top Of The Accepted Export Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_155107`
- round loop: `round 4/17`
- hypothesis: `Round 2/17 established a new accepted base at 25.505328 ms, while round 3/17 showed that further export flattening only regressed by 0.040 ms and pushed long-scoreboard back up to 7.75. That means the export family is no longer the best next lever. The next bounded move should keep the accepted export helper intact and retune the PTX `cp.async` handoff itself, starting with the A/B staging order and future-tile refill sequence, to see whether the remaining scoreboard is now feed latency rather than epilogue control.`
- expected bottleneck: `Copy-pipeline handoff timing in the PTX hot-band steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1975-1989, src/kernels/bf16_gemm_v1.cu:1991-2020, src/kernels/bf16_gemm_v1.cu:1056-1099`
- risk: `Medium. This is a clean family shift on top of the accepted base, but changing the steady-state prefetch order can easily reshuffle barrier and scoreboard stalls without a net runtime win.`
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
