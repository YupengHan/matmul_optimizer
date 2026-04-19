# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Pairwise unroll the peeled 64x384 hot loop without changing the handoff model`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_103511`
- round loop: `round 3/5`
- hypothesis: `The restored 2872f92 winner already proved that deeper single-skew overlap inside the peeled 64x384 hot kernel is useful, but it still only reaches 33.64% tensor active with 15.46% barrier stall and 29.92% mio_throttle. The 3eeb098 named-barrier/subgroup stage-handoff retune is strong negative evidence for adding more handoff state because it dropped the hot kernel to one register-limited block per SM at 167 registers/thread. The best bounded follow-up is to keep the accepted cp.async plus CTA barrier recycle model and process two fixed K tiles per steady-state iteration so the hot loop pays less loop/index overhead per MMA issue.`
- expected bottleneck: `Tensor issue underfill and loop/control overhead inside the fixed 64x384 hot kernel, with register growth as the main guardrail.`
- code locations: `src/kernels/bf16_gemm_v1.cu:573-583, src/kernels/bf16_gemm_v1.cu:588-625, src/kernels/bf16_gemm_v1.cu:627-667`
- risk: `A 2x steady-state unroll can recreate the recent register blow-up; if the hot kernel climbs well above the accepted 128 registers/thread, occupancy will collapse back to the failure mode seen at 3eeb098.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
