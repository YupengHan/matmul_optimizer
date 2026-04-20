# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep The Accepted PTX Branch And Make The Steady-State Sequence More Explicit`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_014548`
- round loop: `round 41/100`
- hypothesis: `The round-40 runtime regression should not be treated as a branch failure. The active PTX hot-band call site in commit 09d3544 is behaviorally identical to the round-38 new-best commit e26d834, and the measured stall mix is effectively the same: tensor-active 47.84 vs 47.87, warps-active 16.51 vs 16.51, barrier 10.96 vs 11.13, short_scoreboard 5.88 vs 5.87, and mio_throttle 0.57 vs 0.55. That means the accepted full B-reuse PTX branch is still the right base. The next move should keep the current two-stage cp.async pipeline, the padded export scratch, and the accepted consumer-side B-reuse pattern intact, but rewrite the active 128x128 K16 PTX hot loop into a more explicit prologue / steady-state / epilogue sequence so the branch pays less control-flow and synchronization overhead per K tile. For this round the primary human-idea family is Stage plus Async Copy plus Pg2s, but only as sequencing cleanup on top of the already-working baseline rather than a deeper-stage rewrite.`
- expected bottleneck: `Synchronization and orchestration overhead in the active PTX steady-state loop. The accepted branch has already collapsed mio_throttle, so the next runtime limiter is the combination of CTA barrier cost and warp-local short scoreboard that comes from the current wait / sync / recursive consume sequence.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1089 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:745 ptx_wmma_accumulate_tile_set_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1026 stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:1039 stage_b_shared_tile_async`
- risk: `Medium. The safest version keeps tile shape, stage depth, and the accepted B-reuse dataflow fixed, but even a sequencing-only cleanup can accidentally reintroduce extra waits, raise register lifetime, or disturb the low-mio behavior that currently makes the PTX branch competitive.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active`

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
