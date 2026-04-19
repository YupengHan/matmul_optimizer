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

- diagnosis id: `diagnosis_20260418_210351`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Async double-buffered K pipeline | bottleneck: Global-memory latency plus CTA-wide synchronization between K-slices, visible as long scoreboard stalls and barrier stalls in the steady-state loop.
- dir_02: Swizzle shared-memory staging for WMMA loads | bottleneck: Shared-memory communication pressure around fragment loads, showing up as MIO throttle and lingering scoreboard stalls even though DRAM is not saturated.
- dir_03: Retile CTA and warp partitioning | bottleneck: Synchronization overhead and low tensor-issue density from the current CTA/warp shape, not raw DRAM bandwidth.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
