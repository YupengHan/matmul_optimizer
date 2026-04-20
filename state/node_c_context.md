# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune PTX Hot-Band Async Stage`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_020307`
- round loop: `round 43/100`
- hypothesis: `The active PTX hot-band path is already functionally equivalent to accepted round-38 commit e26d834 on the active code path, so round 42's 27.003904 ms regression is more consistent with measurement drift than with a dirty source restore. The dominant bottleneck is still the 128x128 PTX hot-band microkernel, which spends nearly all profiled time in a one-K-tile ping-pong loop with full CTA barriers; porting this branch toward the neighboring two-K-tile staged pipeline should cut synchronization tax and feed Tensor Cores more steadily.`
- expected bottleneck: `Synchronization and stage-pipeline overhead in the active hot-band PTX branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1895-1991 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:330-357 cp.async_copy_16_bytes / cp_async_commit_group / cp_async_wait_group_*, src/kernels/bf16_gemm_v1.cu:1648-1778 neighboring fixed_hot_band_128x128 staged kernel with two-K-tile pipeline`
- risk: `Medium. The steady-state schedule changes are localized to the active hot-band branch, but the stage rewrite can introduce correctness bugs or erase overlap if the wait-group ordering is wrong.`
- metrics to re-check: `gpu__time_duration.avg for bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`

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
