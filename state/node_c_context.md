# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 10 Stage: keep the correct hot kernel, but specialize the fixed 452-tile loop into explicit prologue / steady-state / epilogue control`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_210902`
- round loop: `round 6/10`
- hypothesis: `Round 5 proved that changing only the internal 64x64 tile order on the correct branch is too low-signal: overall runtime improved by only about 0.024 ms and the hot-band kernel itself actually moved the wrong way to about 41.11 us. That says the current bottleneck is not a tiny per-fragment order tweak. The better next move is the user's fixed-shape Stage idea: keep the correct 256x128 / 64x64 kernel and the same layout, but rewrite the 452-tile hot loop so most iterations execute in a simpler steady-state form with fewer generic branch checks and cleaner cp.async handoff. This directly targets hot-loop orchestration tax while preserving correctness and shared/register budgets.`
- expected bottleneck: `Generic steady-state loop control and stage-transition overhead in the true hot-band kernel rather than operand layout.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async`
- risk: `The upside is moderate. If the actual wall is still register-limited feed rather than control overhead, this can become a refactor with little runtime impact.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread`

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
