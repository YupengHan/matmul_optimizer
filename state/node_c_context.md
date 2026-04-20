# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the current best branch and raise the hot-band K16 loop to the next small unroll factor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002144`
- round loop: `round 28/50`
- hypothesis: `Round 27 confirmed that the lighter compiler approach to fixed-loop overhead works: restoring the best branch and moving away from `unroll 1` delivered a large gain without disturbing correctness. The next logical move is to stay on that axis and raise the K16 hot-band loop to the next small unroll factor. This keeps the same grouped-order base, the same `launch_bounds(128, 2)` clue, and the same control structure, while giving ptxas more room to schedule across adjacent iterations.`
- expected bottleneck: `Residual loop-control and scheduling overhead in the current best hot-band K16 kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1680`
- risk: `Larger unroll factors can quickly increase register pressure or code size. The gain may flatten or reverse after the first successful step.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
