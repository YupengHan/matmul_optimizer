# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_03`
- direction name: `Fixed-K PTX orchestration retime inside the peeled hot loop`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_132801`
- round loop: `round 3/5`
- hypothesis: `With the PTX branch now using a fully named 12-tile accumulator set, the fixed-K loop structure at src/kernels/bf16_gemm_v1.cu:819-875 is visible enough to retime directly. A bounded next step inside the same branch is to specialize the pairwise steady-state schedule further around the known 452 K-tiles so cp.async commit/wait, stage swap, and the two accumulate calls per loop body leave fewer issue bubbles between compute groups. This does not change the tail or macro tile; it is a PTX-local orchestration refinement on top of the newly stabilized hot-band kernel.`
- expected bottleneck: `Barrier and issue scheduling inside the fixed peeled loop are still interrupting tensor issue, even though the branch has already cut mio versus the WMMA base.`
- code locations: `src/kernels/bf16_gemm_v1.cu:765-818, src/kernels/bf16_gemm_v1.cu:819-860, src/kernels/bf16_gemm_v1.cu:863-875`
- risk: `This keeps the same 172-register live set and therefore may not move the main occupancy guardrail on its own. It also risks chasing small schedule gains after two wins that were more structural than timing-only.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, median runtime`

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
