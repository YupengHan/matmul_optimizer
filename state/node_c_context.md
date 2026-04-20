# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the current best branch and raise the hot-band K16 loop from unroll-1 to a small fixed unroll factor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002004`
- round loop: `round 27/50`
- hypothesis: `Round 26 showed that fully peeling the fixed loop was too invasive for the current best branch, but the motivation behind it still stands: the hot-band K16 mainloop is carrying control overhead. The next lower-risk move is to restore the grouped_rows=8 plus `launch_bounds(128, 2)` winner and let the compiler unroll the fixed K loop by a small factor instead of forcing `#pragma unroll 1`. A factor like 2 keeps the original control structure and wait semantics while still giving ptxas room to remove some branch / scheduling overhead.`
- expected bottleneck: `Loop-control overhead in the accepted hot-band K16 kernel, approached through milder compiler unrolling rather than manual schedule peeling.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1671`
- risk: `Even a small unroll factor can perturb register pressure or code size. The risk is much lower than the peeled-schedule rewrite because the algorithm stays the same.`
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
