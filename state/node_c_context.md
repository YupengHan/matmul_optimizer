# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep grouped_rows=8 and refine the compiler clue to a two-argument launch-bounds target of 2 resident CTAs`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001618`
- round loop: `round 25/50`
- hypothesis: `Round 24 proved that the grouped_rows=8 base plus a single-argument `__launch_bounds__(128)` materially improves codegen: runtime dropped by 1.49 ms, tensor active rose, and the register-limited occupancy signature moved to 2. That makes a two-argument `__launch_bounds__(128, 2)` the most coherent next step. It matches the resident-CTA regime the compiler already appears to prefer, but states it explicitly, which may let ptxas tighten scheduling and allocation a bit further without the catastrophic over-constraint from round 19.`
- expected bottleneck: `Compiler allocation / instruction scheduling quality on the accepted grouped-order hot-band kernel, now that the preferred 2-CTA regime is visible in measured data.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1611`
- risk: `Even though `2` matches the current measured regime, explicit minimum-block guidance can still perturb codegen negatively. The risk is much smaller than the old `4` target but is not zero.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, correctness pass rate`

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
