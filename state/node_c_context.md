# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Tighten PTX Hot-Band Grouping Further To A 2-Row Window`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_163042`
- round loop: `round 12/17`
- hypothesis: `Round 11/17 showed that reopening the grouping family on top of the accepted export base was the right move: the 4-row window cut long-scoreboard to 6.14 and pulled runtime down to 25.40644836 ms, substantially better than the 6-row and 5-row variants, but still short of the accepted base. That makes the next best bounded step a tighter 2-row grouping, which divides the 50 hot-band CTA rows evenly and may preserve the scoreboard gain while reducing the remaining orchestration noise more cleanly than the 4-row remainder case.`
- expected bottleneck: `Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.`
- code locations: `src/kernels/bf16_gemm_v1.cu:155-156, src/kernels/bf16_gemm_v1.cu:1969-1979, src/kernels/bf16_gemm_v1.cu:2097-2104`
- risk: `Medium. The grouping family is trending in the right direction, but over-tightening the window may just swap one orchestration cost for another without beating the accepted base.`
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
