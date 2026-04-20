# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 10/50` with `41` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_230948`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/50 pivots away from warp-local fragment-residency experiments because they have been too fragile on correctness. The recommended next move is therefore dir_01: restore the accepted-correct surface and test a light L2-friendly CTA swizzle, which is the safest remaining human-idea branch with a plausible upside.`
- dir_01: Restore the accepted-correct surface and try a light 4-column serpentine CTA swizzle on the hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band B tiles rather than warp-local tensor scheduling.
- dir_02: Restore the accepted-correct surface and try warp-specialized Pg2s staging without changing the tile shape | bottleneck: CTA-level staging orchestration and barrier dilution inside the hot-band loop.
- dir_03: Restore-only fallback to the accepted best surface | bottleneck: Not a bottleneck attack; this is the fallback reset path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
