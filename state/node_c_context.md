# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Warp-specialize the peeled 64x384 hot loop into producer and consumer warps`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_122507`
- round loop: `round 1/5`
- hypothesis: `The accepted 64x384 base still stages A and B with all eight warps participating equally, then pays CTA-wide handoff points before every stage recycle. With tensor active at 34.86, barrier stall at 15.23, mio_throttle at 35.53, and hot-kernel LSU pressure already high, the limiting symptom looks more like staging plus synchronization diluting tensor issue than macro-tile shape. Keep the single-skew 64x384 layout and reserve 1-2 warps for stage_a_shared_tile_async, stage_b_shared_tile_async, and cp.async commit/wait while the remaining warps stay focused on accumulate_peeled_shared_stage and the MMA loop as much as possible.`
- expected bottleneck: `All-warps staging and CTA-wide stage handoff in the peeled 64x384 hot kernel, which can suppress tensor issue even when occupancy is still healthy at the current 2-block register limit.`
- code locations: `src/kernels/bf16_gemm_v1.cu:236-263, src/kernels/bf16_gemm_v1.cu:599-607, src/kernels/bf16_gemm_v1.cu:611-656, src/kernels/bf16_gemm_v1.cu:658-666`
- risk: `A bad producer/consumer ratio can underfeed the MMA warps or reduce effective active warps without raising tensor issue. Role bookkeeping can also increase registers/thread if it is not kept tight.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, median runtime`

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
