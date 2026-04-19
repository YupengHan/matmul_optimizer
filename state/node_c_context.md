# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Straight-line the Tile384 cp.async producer schedule on the restored base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_123925`
- round loop: `round 3/5`
- hypothesis: `The restored 15d63b2 base still pays fully generic `for (copy_idx = threadIdx.x; ...)` ownership loops for A and B staging even though the hot path uses one fixed 64x384 tile and one fixed K depth. Round 1 showed that warp specialization is the wrong way to attack that overhead because it exploded the hot kernel to 219 registers/thread and collapsed active warps to 16.60. Round 2 showed that lowering barrier and mio in a broader phase split did not automatically produce a win. The best next move is a narrower hot-path simplification: keep all warps symmetric, keep the single-skew 64x384 layout, and replace the generic producer loops with a Tile384-specific cp.async schedule that removes loop and address overhead without changing macro shape or warp roles.`
- expected bottleneck: `Producer-side cp.async issue and LSU address-generation overhead in the 64x384 hot kernel, while preserving the accepted 128-register, 2-block occupancy behavior.`
- code locations: `src/kernels/bf16_gemm_v1.cu:236-263, src/kernels/bf16_gemm_v1.cu:599-607, src/kernels/bf16_gemm_v1.cu:625-649`
- risk: `A bad straight-line mapping can hurt global-to-shared coalescing or increase code size without lowering stalls. It also must not drift back into asymmetric producer/consumer warp roles.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed, sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`

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
