# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Specialize Tile384 cp.async producer assignment in the peeled hot path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_105254`
- round loop: `round 5/5`
- hypothesis: `The accepted best 8346b48 already restored the right hot-loop shape: pairwise peeled steady-state compute, 128 registers/thread, and a stable 2-block register occupancy limit. The edb3741 skew-retune is explicit negative evidence against further B-layout tweaking because runtime regressed while mio_throttle stayed flat-to-worse and the hot kernel's LSU wavefront pressure jumped instead of falling. The best bounded next move is therefore to leave the accepted single-level B layout and CTA-wide recycle model intact, but replace the generic stage_a_shared_tile_async and stage_b_shared_tile_async ownership loops with a Tile384-specific producer schedule so cp.async issue and address work are straighter and cheaper in the hot path.`
- expected bottleneck: `Producer-side cp.async issue overhead and LSU address-generation pressure in the 64x384 peeled hot kernel, not occupancy or synchronization.`
- code locations: `src/kernels/bf16_gemm_v1.cu:236-263, src/kernels/bf16_gemm_v1.cu:599-607, src/kernels/bf16_gemm_v1.cu:625-649, src/kernels/bf16_gemm_v1.cu:709-762`
- risk: `A bad producer partition can break global-to-shared coalescing or add enough control flow to erase the gain. It also must not increase registers/thread enough to lose the accepted 2-block occupancy limit.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`

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
