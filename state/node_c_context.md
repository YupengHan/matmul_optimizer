# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: continue the half-panel family, but spend this round on correctness root-cause repair while preserving the 92-reg / 2-block signal`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_194057`
- round loop: `round 18/20`
- hypothesis: `With only three rounds left, the half-panel family is still worth continuing because it remains the only branch that has actually punctured the register wall and then recovered runtime toward the accepted base. The current hot kernel is already down to 92 registers per thread, occupancy_limit_registers is 2, active warps stay around 32.70, tensor active is up to 43.55, and the hot-kernel time improved again from round 17. That signal is too strong to abandon. The right next move is not A-side compaction yet; it is a correctness-first repair that freezes the winning occupancy shape and audits the remaining pass-local half-panel plumbing end to end. The most concrete one-round action is to make half-panel identity single-sourced and explicit across the local MMA tiles, compact B shared layout, and export path: thread a compile-time HalfPanelColBase layout helper through ptx_wmma_mma_row_pair_64x32, ptx_wmma_accumulate_tile_set_64x32, stage_b_half_panel_shared_tile_async, and ptx_wmma_store_tile_pairs_64x32 so no address arithmetic is duplicated ad hoc. The current code has already fixed one obvious double-offset bug, but correctness still fails badly, which strongly suggests there is still a remaining panel-identity mismatch somewhere in this pass-local plumbing.`
- expected bottleneck: `Correctness bug in the half-panel pass-local mapping and orchestration, not lack of more occupancy or more feed bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:647-710, src/kernels/bf16_gemm_v1.cu:890-955, src/kernels/bf16_gemm_v1.cu:996-1102, src/kernels/bf16_gemm_v1.cu:1594-1619`
- risk: `This is a correctness-first round, so it can easily produce only a small runtime move even if it succeeds. The other risk is that a broad refactor of half-panel layout logic could accidentally lose the current 92-register / 2-block occupancy signal if extra state is introduced.`
- metrics to re-check: `correctness cases, median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`

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
