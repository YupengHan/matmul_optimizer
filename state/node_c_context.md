# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the 26.924 ms 128x128 K16 base and open an active hot-band PTX microkernel branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_005302`
- round loop: `round 35/100`
- hypothesis: `The real active 256x128/64x64 promotion already rejected further Tiling-first work on this branch: compared with the accepted 26.924031 ms 128x128 K16 base, tensor-active fell from 48.56% to 36.60% while DRAM and L2 also fell, so the regression is feed/orchestration on the active hot band rather than global bandwidth. The highest-ceiling remaining move is to restore the accepted 128x128 K16 default launch, keep the tail and peeled remainder unchanged, and split the 6400x7680 hot band onto a PTX microkernel path with explicit consumer load order, `mma.sync` sequencing, warp-local register reuse, and a lighter export path so fragment residency and operand delivery are no longer constrained by the current WMMA control surface.`
- expected bottleneck: `Tensor Core under-utilization caused by active hot-band consumer feed, fragment scheduling, and export overhead on the current accepted path; this is the remaining family with enough upside to move from 26.9 ms toward the 20 ms target.`
- code locations: `src/kernels/bf16_gemm_v1.cu:384, src/kernels/bf16_gemm_v1.cu:407, src/kernels/bf16_gemm_v1.cu:608, src/kernels/bf16_gemm_v1.cu:809, src/kernels/bf16_gemm_v1.cu:1630, src/kernels/bf16_gemm_v1.cu:1776`
- risk: `Highest implementation risk of the three directions: explicit PTX MMA/load/export control can easily break correctness, raise register pressure, or lose occupancy if the first branch is too ambitious. Keep it bounded to the restored active 128x128 K16 hot band only and leave the remainder and tail paths untouched.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers`

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
