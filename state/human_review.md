# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 7/20` with `14` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_231124`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Restore the low-footprint wide B slab and keep any new swizzle occupancy-neutral | bottleneck: Shared-memory footprint and B-fragment load efficiency are cutting block residency and leaving the tensor loop underfed.
- dir_02: Retune the CTA and per-warp N tile so B-side experiments do not burn residency | bottleneck: Occupancy and latency hiding are constrained by the current CTA tile shape and its shared-memory budget.
- dir_03: Specialize the fixed-shape mainloop so the async pipeline pays less per-step control and sync overhead | bottleneck: Synchronization and fixed-shape control overhead in the steady-state async-copy and MMA loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
