# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the current best grouped K16 branch and test the intermediate unroll factor between 2 and 4`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002530`
- round loop: `round 30/50`
- hypothesis: `The unroll sweep now has a clear pattern: `unroll 2` improved the best branch substantially, while `unroll 4` overshot and regressed. That strongly suggests the remaining optimum may sit between them. Because `#pragma unroll` accepts arbitrary small factors, the next rational step is to restore the grouped_rows=8 plus `launch_bounds(128, 2)` K16 winner and test `unroll 3`. This keeps the entire winning branch intact and only probes the unroll midpoint that we have not measured yet.`
- expected bottleneck: `Loop-control / scheduling overhead in the current best hot-band K16 kernel, with the unroll factor now being the only moving part.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1680, src/kernels/bf16_gemm_v1.cu:1780`
- risk: `The gain may be negligible if `unroll 2` is already optimal. There is still some risk of extra register pressure versus the current best.`
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

- no tracked dirty paths at prepare time
