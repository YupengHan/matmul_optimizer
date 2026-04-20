# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the current best branch and peel the fixed 452-tile K loop into steady-state plus epilogue`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001749`
- round loop: `round 26/50`
- hypothesis: `The current best branch has already validated the CTA-order and compiler-clue ideas, and it is now close enough to CUTLASS that control overhead becomes worth attacking directly. The hot-band kernel still runs a generic loop with per-iteration branch checks for future-stage existence and wait behavior, even though the benchmark K dimension is fixed at 452 K16 tiles. Peeling the 452-tile loop into a long steady-state section with unconditional future-stage staging, followed by a short explicit epilogue for the final two tiles, should reduce loop-control overhead without changing shared footprint or the accepted grouped-order / launch-bounds base.`
- expected bottleneck: `Mainloop control-flow and stage-transition overhead inside the accepted hot-band kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1666, src/kernels/bf16_gemm_v1.cu:1681, src/kernels/bf16_gemm_v1.cu:1694`
- risk: `This is more invasive than the last few rounds. A mistake in the peeled epilogue can silently break correctness even if the steady-state body is sound.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
