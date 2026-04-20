# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the peeled steady state, but restore the proven final-two-tile handoff to recover correctness`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_225521`
- round loop: `round 5/50`
- hypothesis: `Round 4 produced the clearest positive runtime signal in many rounds: the dominant 256x128 hot-band kernel dropped from 41.080 ms to 40.365 ms and tensor activity rose from 38.75% to 39.28%. That means the fixed-shape steady-state peeling direction is probably correct, but the manual epilogue around the last two K-tiles is not. Instead of abandoning the direction, the next move should keep the branch-free steady-state core and hand the last two iterations back to the original, already-correct next/future/wait0 control sequence. This preserves almost all of the control-flow win while removing the highest-risk cp.async boundary change.`
- expected bottleneck: `Correctness break in the final cp.async stage handoff of the peeled hot-band schedule, not a failure of the hot-band steady-state peeling idea itself.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_64x64_kernel`
- risk: `Moderate but targeted. The performance gain is already measured, and the likely fix surface is the last-two-tile control handoff rather than a full rollback.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread`

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
