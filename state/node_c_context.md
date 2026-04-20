# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_112500`
- round loop: `round 74/100`
- hypothesis: `The latest run is still compute/schedule limited rather than memory bound: tensor activity is 48.21%, SM throughput is 47.80%, warps active are only 16.57%, and launch occupancy is still limited by registers. The hottest measured kernel is the 128x128 PTX microkernel, so the best next move is to keep its semantics fixed and flatten the recursive PTX compute helpers that feed the accepted row-pair / column issue order. That should shorten live ranges, reduce compiler scheduling friction, and give the same math a better chance to run with more resident warps.`
- expected bottleneck: `Register pressure and compiler scheduling friction inside the active PTX hot-band compute path, which is consistent with launch__occupancy_limit_registers = 2 and the low achieved warps-active number.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-781, src/kernels/bf16_gemm_v1.cu:1908-2012`
- risk: `Medium. This is the most direct way to attack the register-limited profile, but it can easily turn into a no-op if the helper flattening does not materially change live ranges or PTX codegen.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
