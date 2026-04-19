# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/5` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_210931`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Reduce cp.async barrier pressure | bottleneck: Barrier and wait-group serialization in the double-buffered steady-state loop.
- dir_02: Widen and repack the staging path | bottleneck: MIO throttle from cp.async issue rate and shared-memory staging layout.
- dir_03: Retune the tensor block geometry | bottleneck: Occupancy / register pressure limiting tensor-core issue efficiency.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
