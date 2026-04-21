# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_184122`
- round loop: `round 7/50`
- hypothesis: `The latest measured run 20260420_184055_bf16_gemm_v1_9144f92 rejects the reopened 256x128 auxiliary branch as the next default path: the hot-band kernel alone took 40.086 ms versus 32.802 ms on the accepted 2e4dd24 base, tensor active dropped from 48.16% to 39.55%, barrier stalls jumped from 5.61% to 21.84%, and correctness failed on all 3 cases. The best next move is to keep the accepted grouped-row locality idea but remove the wide-CTA branch that introduced the barrier wall. The existing non-PTX 128x128 sibling is the cleanest control-family pivot because it already has correct measured ancestry, and porting the grouped-row physical-to-logical traversal into it is the most credible way to preserve locality without the broken 256x128 schedule.`
- expected bottleneck: `If the grouped-row port is incomplete, the sibling kernel will likely give back L2 reuse and shift the bottleneck from barrier stalls to long-scoreboard or memory-latency stalls. The target is lower barrier share without collapsing cache behavior relative to the accepted grouped PTX base.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1836-1937, src/kernels/bf16_gemm_v1.cu:1938-1976, src/kernels/bf16_gemm_v1.cu:2078-2125`
- risk: `Medium. Historical measured evidence for the plain two-stage sibling is only mid-25 to high-26 ms, so this is not a proven winner by itself, but it is the lowest-risk new family after the latest 256x128 correctness failure and avoids repeating the same PTX inner-loop experiments that already regressed in rounds 3 through 5.`
- metrics to re-check: `correctness pass rate across all 3 cases, median_runtime_ms, hot-band kernel gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
