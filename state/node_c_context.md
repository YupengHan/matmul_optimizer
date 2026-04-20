# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Revisit the 128x128x32 hot-band branch on top of the current grouped-order plus launch-bounds base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_002345`
- round loop: `round 29/50`
- hypothesis: `Earlier 128x128x32 attempts were measured before the grouped-order and compiler-clue improvements that define the current best branch. Those changes materially altered the residency regime: the current winner already runs in a 2-CTA register-limited mode, which narrows the occupancy disadvantage that previously hurt K32. That makes it worth re-testing the 128x128x32 branch with the same grouped CTA order and the same mild `launch_bounds(128, 2)` guidance, because K32 still offers the best chance to reduce mainloop control overhead if its old occupancy penalty is no longer the dominant cost.`
- expected bottleneck: `Stage-depth / control-overhead tradeoff under the new best branch conditions, not under the older pre-grouped baseline.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1472, src/kernels/bf16_gemm_v1.cu:1501, src/kernels/bf16_gemm_v1.cu:1780`
- risk: `Shared footprint is still higher than K16, so K32 may remain slower even in the new regime. This is a deliberate re-test, not a guaranteed promotion.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, launch__occupancy_limit_registers, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
