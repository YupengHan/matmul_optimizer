# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/5` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_132801`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_03`
- diagnosis notes: `All three directions stay strictly inside the 64x384 hot-band PTX microkernel branch and keep the 64x96 tail unchanged. Ranking explicitly uses the new fact that the PTX line has now delivered two consecutive real runtime improvements, including the round-2 win from replacing the array-style accumulator surface with 12 named tiles and compile-time expansion. Because occupancy_limit_registers is still 1 and active warps are still only 16.78, the next ranking prefers deeper PTX-local compute/load-order and live-state control over any switch back to WMMA or unrelated tile tuning.`
- dir_01: Ldmatrix plus panelized PTX hot-band compute control | bottleneck: Register-limited live state inside the current PTX hot-band compute path is holding occupancy at one block/SM; the branch now needs finer compute/load-order control to reduce residency pressure without abandoning the winning PTX line.
- dir_02: Register-first PTX export follow-through | bottleneck: The hot-band export path is still consuming shared/LSU issue budget and can now be a larger share of the remaining cost because mio throttle has already dropped sharply while runtime continues to improve.
- dir_03: Fixed-K PTX orchestration retime inside the peeled hot loop | bottleneck: Barrier and issue scheduling inside the fixed peeled loop are still interrupting tensor issue, even though the branch has already cut mio versus the WMMA base.

## Active direction

- selected direction: `dir_03`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
