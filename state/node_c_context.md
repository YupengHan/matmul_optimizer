# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore grouped_rows=8 and try a single-argument launch-bounds clue on the accepted hot-band kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001453`
- round loop: `round 24/50`
- hypothesis: `The grouped-order search now has enough shape to lock in `grouped_rows=8` as the current best L2 setting: both 16 and 4 were worse. That lets us keep the accepted L2 base and revisit the Register-Reuse / compiler-guidance axis in a much safer form than round 19. A single-argument `__launch_bounds__(128)` tells ptxas the real launch width of the hot-band kernel without demanding extra resident blocks, so it is the narrowest reusable compiler clue worth testing next.`
- expected bottleneck: `Compiler allocation / scheduling quality on top of the accepted grouped-order 128x128 K16 kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:141, src/kernels/bf16_gemm_v1.cu:1611`
- risk: `The hint may do nothing at all, or it may still perturb codegen negatively. The risk is lower than round 19 because it does not encode a minimum resident-block target.`
- metrics to re-check: `median runtime, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness pass rate`

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
