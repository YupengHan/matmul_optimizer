# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 5 Bank conflict fallback: restore the accepted 64x384 base and try a warp-local B-consumer transform with zero extra CTA repack`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_200532`
- round loop: `round 20/20`
- hypothesis: `Round 18 and round 19 proved that the half-panel family has real occupancy upside, but they also proved that it is not a one-round-away correct branch: round 19 still failed all correctness cases, regressed to 31.338 ms, and only improved the error shape rather than clearing it. With one round left, the right move is to return to the last correct accepted base b13027c at 30.0528 ms and spend the final implementation budget on the user's strict B-feed rule: attack the B consumer layout at the warp boundary only, without a second shared tile, without new CTA barriers, and without reducing stage depth. The measured accepted-base history already says 64x384 is the best correct tile width on this GPU and shape, so the final round should be a correct-branch feed experiment rather than another correctness rescue on the half-panel branch.`
- expected bottleneck: `Shared/L1/bank behavior on the stable 64x384 hot path rather than occupancy. The goal is to improve operand delivery without destabilizing correctness.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_384, src/kernels/bf16_gemm_v1.cu:accumulate_peeled_shared_stage_ptx, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_peeled_kernel`
- risk: `This is lower risk than continuing half-panel, but it is also lower ceiling. The final round may still finish near the accepted base rather than materially below it.`
- metrics to re-check: `correctness, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, shared mem / block allocated`

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
