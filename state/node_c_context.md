# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Split the fixed 64x384 hot path into explicit prologue, steady-state, and epilogue phases`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_123318`
- round loop: `round 2/5`
- hypothesis: `On the restored 15d63b2 base, the hot kernel is already fixed-shape but still pays generic inner-loop control each pair of K tiles: `tile_idx` induction, `first_future_tile_k` and `second_future_tile_k` arithmetic, `curr_stage` and `next_stage` swapping, repeated wait and barrier sequencing, and a generic final drain path. Since the benchmark shape is fixed at 6464 x 7776 x 7232 with exactly 452 K tiles and a fixed 64x384 hot band plus 64x96 tail, split the peeled kernel into explicit prologue, compile-time steady-state batches, and epilogue logic so the steady-state body is just the known stage-advance sequence rather than a generic loop. This targets control-flow and stage-transition overhead without changing the macro shape or memory volume.`
- expected bottleneck: `Fixed-shape hot-loop control and stage-transition overhead in the restored 64x384 peeled kernel, where tensor activity is still only 34.86 despite stable 2-block occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:559-567, src/kernels/bf16_gemm_v1.cu:599-609, src/kernels/bf16_gemm_v1.cu:611-666, src/kernels/bf16_gemm_v1.cu:728-761`
- risk: `The ceiling is lower than the failed warp-specialization path, and over-unrolling the steady-state schedule could still bloat registers if the phase split is too aggressive. The implementation needs to preserve the current 128-register, 2-block occupancy behavior.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, median runtime`

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
