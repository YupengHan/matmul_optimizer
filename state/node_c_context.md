# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Activate The Dormant 128x128x32 Hot-Band Branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_174253`
- round loop: `round 1/50`
- hypothesis: `No new explicit human-review idea family is queued in state/human_review.md, so the ranking is driven by the measured run itself. The latest hybrid prefetch permutation improved runtime from 25.62406445 ms to 25.47660828 ms and cut the dominant hot-band kernel's barrier stall from 6.63 to 5.52 while trimming registers from 202 to 200, but the same hot-band launch still dominates at 32.97 ms with only 16.54% active warps, 47.72% tensor activity, and a worse 8.02% long-scoreboard stall. That means the prefetch-order family is likely exhausted. The next best move is to change staging granularity, not another A/B ordering tweak: switch the hot band to the existing 128x128x32 kernel so each stage covers 32 K values and halves the steady-state handoff frequency on the same 128-thread CTA shape.`
- expected bottleneck: `Synchronization and latency-hiding limits in the current 128x128 K16 hot-band cadence, especially the two-block occupancy ceiling and rising long-scoreboard stalls.`
- code locations: `src/kernels/bf16_gemm_v1.cu:149-156, src/kernels/bf16_gemm_v1.cu:1687-1843, src/kernels/bf16_gemm_v1.cu:2077-2114`
- risk: `Medium-high. This is a structural hot-band branch and earlier K32 work carried correctness risk, but the kernel already exists in the current source and it is the highest-upside family that directly attacks the measured occupancy and handoff problem.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread`

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
