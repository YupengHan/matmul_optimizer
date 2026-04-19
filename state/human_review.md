# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 1/5` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_122507`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Diagnosed accepted base run 20260419_122438_bf16_gemm_v1_15d63b2 at 35.725824 ms. The human-priority direction is ranked first and recommended: keep the single-skew 64x384 macro tile and test a warp-specialized producer/consumer split in the peeled hot kernel. The current measured bottlenecks are coherent with that choice: tensor active remains only 34.86 while barrier stall is 15.23, mio_throttle is 35.53, and hot-kernel LSU pressure is already high. The other two directions stay bounded and avoid reopening macro-tile changes.`
- dir_01: Warp-specialize the peeled 64x384 hot loop into producer and consumer warps | bottleneck: All-warps staging and CTA-wide stage handoff in the peeled 64x384 hot kernel, which can suppress tensor issue even when occupancy is still healthy at the current 2-block register limit.
- dir_02: Pair Tile384 epilogue export across the existing two C-scratch stages | bottleneck: Hot-kernel shared export and LSU traffic after MMA completion, which can still contribute to the current mio_throttle even when the main loop is well scheduled.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop, barrier, and scoreboard overhead in the 64x96 tail kernel; upside is capped because the tail is only a small share of total wall time.

## Active direction

- selected direction: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
