# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Use The Non-PTX 128x128 Sibling As The Next Control Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_162446`
- round loop: `round 10/17`
- hypothesis: `Round 9/17 showed that reopening the PTX prefetch family on top of the new export base does improve the failed round-8 variant, but it still cannot beat the accepted base because it only trades long-scoreboard down to 6.58 for a higher barrier cost of 6.68. That effectively closes the reopened PTX prefetch family. The best next move is now the non-PTX 128x128 sibling control: it keeps the same hot-band tile geometry while removing the PTX-specific export/store and refill interaction that is now dominating the remaining tradeoff.`
- expected bottleneck: `PTX-specific export/store and refill interaction versus the simpler non-PTX 128x128 sibling path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1848-1932, src/kernels/bf16_gemm_v1.cu:2096-2104`
- risk: `Low to medium. This is a bounded control-path switch that preserves the same 128x128 shape, but it may simply underperform the accepted PTX base if the remaining cost is not PTX-specific.`
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

- no tracked dirty paths at prepare time
