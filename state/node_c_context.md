# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the grouped CTA-order remap and reduce the hot-band row-group size to check the other side of the L2 curve`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001328`
- round loop: `round 23/50`
- hypothesis: `Round 21 with grouped_rows=8 improved the baseline, while round 22 with grouped_rows=16 regressed. The fastest way to identify whether 8 is already near the local optimum is to probe the opposite side of the same L2-family tuning curve. Reducing the hot-band grouped-row size to 4 will shorten each B-reuse window and show whether the round-21 gain came from moderate grouping specifically or whether a smaller group balances A and B locality better on this grid.`
- expected bottleneck: `Cross-CTA cache locality on the accepted grouped-order hot-band kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:141, src/kernels/bf16_gemm_v1.cu:1635`
- risk: `This may simply give back the round-21 win. The point of the round is to bracket the grouped-order optimum, not to assume the smaller group is better.`
- metrics to re-check: `median runtime, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness pass rate`

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
