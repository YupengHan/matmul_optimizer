# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retry PTX Hot-Band Grouping With A 4-Row Window`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_162714`
- round loop: `round 11/17`
- hypothesis: `Round 10/17 closed the non-PTX 128x128 sibling decisively: it preserved correctness but blew DRAM up to 34.17 and regressed runtime to 26.70438385 ms, so the path away from the PTX microkernel is not competitive. That pushes the search back to the surviving PTX-adjacent levers on top of the accepted export base. The prior grouped-row retune to 5 was measured before the new export cleanup became the accepted baseline. Reopening the grouping family with a 4-row window is the next best bounded move because it keeps the proven PTX/export path intact while retesting CTA orchestration with a more symmetric grouping size than 5.`
- expected bottleneck: `CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.`
- code locations: `src/kernels/bf16_gemm_v1.cu:155-156, src/kernels/bf16_gemm_v1.cu:1969-1979, src/kernels/bf16_gemm_v1.cu:2097-2104`
- risk: `Medium. The family already posted one losing attempt at 5 rows, but the accepted base has changed since then and a 4-row window is closer to the old grouped baseline than the rejected 5-row retune.`
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

- `src/kernels/bf16_gemm_v1.cu`
