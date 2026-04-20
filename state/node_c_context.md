# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Activate The Existing 128x128 Two-Stage Hot-Band Kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_114507`
- round loop: `round 79/100`
- hypothesis: `The staged K32 family is now closed-negative, but the simpler 128x128 two-stage sibling is still a distinct PTX-adjacent family that can reduce barrier and scoreboard pressure while keeping the restored hot-band baseline structure intact.`
- expected bottleneck: `Residual synchronization and latency-hiding overhead in the hot-band steady state, with lower occupancy pressure than the failed K32 staging variant.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1822-1920, src/kernels/bf16_gemm_v1.cu:2044-2105`
- risk: `Medium. It is adjacent to the current restored baseline and may still inherit the same launch geometry limits, but it is materially different from the closed K32 staged family.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`

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
