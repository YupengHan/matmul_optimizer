# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the grouped CTA-order remap and increase the hot-band row-group size to deepen B-tile reuse`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001157`
- round loop: `round 22/50`
- hypothesis: `Round 21 validated the L2-family idea: grouped CTA order improved runtime without changing the inner pipeline. That means the next most efficient move is to stay on the same axis and tune the grouping granularity rather than abandon it after the first positive result. Increasing the hot-band grouped-row count from 8 to a larger value should keep each physical launch batch on the same B tiles for longer, which may improve cross-CTA L2 reuse further on this fixed 60x50 tile grid.`
- expected bottleneck: `Cross-CTA B reuse / L2 locality rather than CTA-local staging or occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:141, src/kernels/bf16_gemm_v1.cu:1635`
- risk: `Too-large groups can swing too far toward one operand and lose the balance that made the first grouped-order change work. The effect may be modest and noisy.`
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
