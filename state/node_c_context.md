# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore grouped_rows=8, then align PTX export order with the reversed compute row-pair traversal`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_091814`
- round loop: `round 65/100`
- hypothesis: `Goal remains sub-20 ms, but the accepted best is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. The current source run is round 64 at 25.56057644 ms only because kFixedHotBandPtxGroupedRows moved from the accepted 8 down to 6; it is a regression family, not a new base. Compared with round 58, the hot PTX 128x128 microkernel kept the same occupancy shape and resource footprint while regressing kernel time from 32.715296 ms to 32.925664 ms and raising DRAM from 9.75 to 11.58, barrier stall from 5.04 to 5.35, and long scoreboard from 7.31 to 7.69. The accepted base characteristics should therefore be restored first: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX row-pair traversal, one-sync steady-state handoff, B-first refill, and active-loop unroll 2. Once that accepted base is back, the cleanest bounded next move is to align the PTX export/live-range order with the already reversed compute traversal. The current compute helper visits higher row-pairs first, but the PTX store helper still exports TileRow 0, then 1, then 2, then 3. Reversing or pairing the export traversal to match compute order is a local epilogue/live-range experiment that stays on the accepted base without reopening grouped_rows retunes, feed-path rewrites, or extra-live Ps2r branches.`
- expected bottleneck: `PTX hot-band export/writeback ordering and accumulator live-range mismatch after the accepted grouped_rows=8 locality base is restored.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:750-778, src/kernels/bf16_gemm_v1.cu:983-1023, src/kernels/bf16_gemm_v1.cu:1934-2014`
- risk: `Moderate. The change is correctness-sensitive because it touches export order, but it is still a bounded, code-local move that leaves shared layout, 64x64 warp ownership, B-first refill, stage depth, and unroll 2 intact.`
- metrics to re-check: `median_runtime_ms against both 25.56057644 ms and the accepted 24.57088089 ms base, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, correctness on all fixed BF16 cases`

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
