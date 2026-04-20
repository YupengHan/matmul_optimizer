# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Apply The Full PTX Prefetch Retime On The Accepted Export Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_163934`
- round loop: `round 16/17`
- hypothesis: `Round 15/17 closed the deeper seam shift: moving the pivot from 6144 to 5888 was worse, so the best seam member is already known. That leaves one last untested PTX family variant with a plausible upside: the full prefetch retime on top of the accepted export base, where both the initial two staging commits and the future refill use A-before-B ordering. Round 9 only tested the narrower future-refill retime. The full variant is the last meaningful scoreboard-oriented move still missing from the accepted export baseline.`
- expected bottleneck: `Copy-pipeline handoff timing across both the initial stage prime and the future-tile refill in the PTX hot-band steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1995-2006, src/kernels/bf16_gemm_v1.cu:2031-2039`
- risk: `Medium. The family already had mixed results, and a full retime can again trade lower scoreboard for higher barrier, but this exact variant has not been tested on the accepted export base.`
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
