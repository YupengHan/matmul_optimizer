# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Try The 128x128x32 Staged Hot-Band Family`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_114200`
- round loop: `round 78/100`
- hypothesis: `The restored PTX baseline is back in the same source surface as the earlier round-74 code, but the present environment is still slower at 25.97375965 ms and the profile remains barrier- and scoreboard-heavy. The most concrete next family is to change staging granularity rather than relitigate dispatch promotion: the 128x128x32 path keeps the restored hot-band semantics but breaks the work into 32-K-slice stages. That gives a plausible route to lower live-range pressure and barrier cost without reopening the closed non-PTX default promotion family.`
- expected bottleneck: `Barrier cost, short-scoreboard pressure, and register/occupancy pressure in the current 128x128 PTX hot-band cadence.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1667-1815, src/kernels/bf16_gemm_v1.cu:2070-2093`
- risk: `Medium. This is a structural change, but it is still anchored to the restored baseline and is more defensible than another baseline-restore round.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
