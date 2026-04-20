# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the 128x128 K16 winner and add a register-pressure / launch-bounds hint to chase higher occupancy`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_000335`
- round loop: `round 19/50`
- hypothesis: `The last two rounds made the tradeoff clear: once hot-band shared memory grows from 26 KB to roughly 42-43 KB per block, active warps collapse and runtime regresses. That means the 29.20 ms 128x128 K16 kernel is still the right base, and the next plausible gain comes from register-side pressure rather than more shared staging. The recommended move is to restore the corrected 128x128 K16 default launch and add an explicit launch-bounds style occupancy hint on that kernel so ptxas has a reason to trim per-thread register usage if possible. This directly reflects the human Register Reuse idea while preserving the async-copy / shared-reuse / stage contract that already won.`
- expected bottleneck: `Register-limited occupancy in the accepted 128x128 K16 hot-band kernel. The target is to increase resident blocks or at least reduce register pressure enough to lift warps active and tensor active.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1609, src/kernels/bf16_gemm_v1.cu:1754`
- risk: `If the compiler satisfies the launch-bounds hint with spills instead of real register trimming, the kernel can slow down even while nominal occupancy improves. The direction is still bounded because it keeps the proven 128x128 K16 algorithm and touches only compiler guidance plus the launch choice.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
