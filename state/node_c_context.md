# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the current best branch and reduce grouped_rows one more step to 2`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002827`
- round loop: `round 32/50`
- hypothesis: `Primary human-idea family for round 32: `L2 Cache`. Grouped CTA ordering is still actively moving in the newer `__launch_bounds__(128, 2)` plus unroll-2 regime: `grouped_rows=4` is now materially better than the earlier `8`. That means the L2 locality sweet spot may still be on the smaller-group side. The bounded next move is to take one more step down to `grouped_rows=2` while explicitly holding the already-accepted base families fixed: wide coalesced global access, shared-memory A/B reuse, async-copy Pg2s staging, the current stage depth, and the existing bank-conflict-safe shared layout.`
- expected bottleneck: `Cross-CTA cache locality under the current best compiler-guided hot-band branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:145`
- risk: `At some point the group gets too small and the B-reuse window collapses. This round is a direct check for that point.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
