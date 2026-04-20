# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The 64x384 Hot-Band Dispatch And Retune Around The Wide-Tile Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_113007`
- round loop: `round 75/100`
- hypothesis: `The round-74 PTX helper flattening family is now effectively closed-negative: the latest run moved only from 24.69619179 ms to 24.6968317 ms and the tensor, warps-active, barrier, and scoreboard metrics stayed essentially flat. The next materially different move is to stop spending effort inside the PTX helper recursion and re-center the hot band on the widest non-PTX dispatch family that already showed strong behavior in the earlier tile sweep, namely the 64x384 path. That should cut launch count, keep the hot band on a lower-overhead schedule, and give the register-limited profile a better chance to improve without changing the accepted PTX traversal semantics.`
- expected bottleneck: `Register pressure and launch/schedule overhead in the current PTX hot-band path, which is consistent with the low 16.57 warps-active number and the register occupancy limit.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1181-1227, src/kernels/bf16_gemm_v1.cu:2042-2058`
- risk: `Medium. This is the most grounded non-PTX alternative because it follows the measured wide-tile family rather than another helper rewrite, but it still has to prove that the dispatch change is worth the additional code-path complexity.`
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
