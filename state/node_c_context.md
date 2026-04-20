# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 sparse-error repair: keep the half-panel branch, but fix the remaining nondeterministic ownership/overlap bug end to end`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_205559`
- round loop: `round 3/10`
- hypothesis: `Round 2 preserved the only real register-wall breakthrough in the repo: the true hot-band kernel dropped from about 41.03 us to 36.94 us, registers/thread fell from 167 to 93, occupancy_limit_registers rose from 1 to 2, and active warps / tensor active both jumped into the low-30s / low-40s. That is too much real signal to abandon with seven rounds still available. The blocker is correctness. The key new clue is that a local rerun of the same correctness case after round 2 moved the max-error index and value, while the mean_abs_err stayed near 0.033. That is not the signature of one fixed deterministic address formula; it points to a sparse nondeterministic ownership or overlapping-writer bug somewhere in the half-panel control/export contract. The next move should therefore keep the half-panel family but tighten ownership all the way through pass control, compact B staging, and global export so each output tile has one compile-time writer and one compile-time column identity.`
- expected bottleneck: `Correctness-blocking nondeterministic ownership/coverage bug in the half-panel control/export path, not DRAM bandwidth or the macro tile choice. Success means the same correctness case stops drifting across reruns while preserving the 93-reg / 2-block occupancy signal.`
- code locations: `src/kernels/bf16_gemm_v1.cu:HalfPanelIdentity64x32, src/kernels/bf16_gemm_v1.cu:stage_b_half_panel_shared_tile_async, src/kernels/bf16_gemm_v1.cu:ptx_export_shared_tile_quads_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_run_half_panel_pass_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_run_half_panel_control_64x32, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Another repair round can still end with an incorrect kernel if the overlap is deeper than the current ownership helpers imply. The guardrail is to avoid silently re-expanding the live set or undoing the 2-block occupancy gain while chasing correctness.`
- metrics to re-check: `correctness_case_* max_abs_err / mean_abs_err, same-case rerun stability of max_abs_index / max_abs_output, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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

- `include/runner_contract.h`
- `src/kernels/bf16_gemm_v1.cu`
- `src/runner/main.cpp`
