# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: keep the half-panel family and close the remaining correctness gap by single-sourcing warp ownership end to end`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_195407`
- round loop: `round 19/20`
- hypothesis: `The latest run keeps the only real register-wall breakthrough in the repo: 30.236 ms despite correctness failure, 43.66% tensor active, 32.90% active warps, and launch__occupancy_limit_registers still at 2. That signal is too strong to abandon with two rounds left. The measured error remains large across all three correctness cases, so the next move should still be correctness-first, but more structural than round 18's local cleanup: make the half-panel path use one compile-time ownership contract for local tile columns from B staging through MMA and shared-export, and remove the remaining duplicated pass-local address arithmetic so warp_tile_n, HalfPanelColBase, accumulator slot, and global C store target cannot drift. If needed, collapse the two launch-site pass calls into one templated local-half loop so the left and right 32-column panels are produced by the same control skeleton instead of two partially duplicated call sites.`
- expected bottleneck: `Residual half-panel address-contract mismatch in the shared-to-fragment or fragment-to-export path, not DRAM bandwidth. The runtime and occupancy signal say the family is viable; correctness is the blocking bottleneck.`
- code locations: `src/kernels/bf16_gemm_v1.cu:HalfPanelIdentity64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x32, src/kernels/bf16_gemm_v1.cu:ptx_export_shared_tile_quads_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x32, src/kernels/bf16_gemm_v1.cu:ptx_wmma_run_half_panel_pass_64x32, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Another narrow fix could still miss the true mismatch and spend the penultimate round without producing a correct kernel. The guardrail is to keep the 92-100 reg regime and reject any repair that silently re-expands the live set.`
- metrics to re-check: `correctness_case_* max_abs_err / mean_abs_err, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
