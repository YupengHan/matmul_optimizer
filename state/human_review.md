# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 20/50` with `31` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_000825`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 20: Stage remains the primary family, but in a deliberately conservative form because the last two aggressive experiments failed for different reasons. Register Reuse is temporarily deferred after round 19 showed that forcing higher occupancy through launch-bounds was far too expensive. Tiling 256x128 is now rejected for the current branch because it raised shared footprint and reduced active warps without any upside. Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background mechanisms already present in the accepted 128x128 K16 kernel. Coalescing Access and Bank Conflict remain deferred because the regressions were driven much more by occupancy / stage effects than by those signals. The L2 clue stays as the next orthogonal backup plan.`
- dir_01: Restore the accepted 128x128 K16 base and scope the consume fence only to real stage overwrites | bottleneck: Barrier / orchestration overhead in the accepted 128x128 K16 hot-band loop, with no increase in shared footprint or register pressure.
- dir_02: Restore the accepted base and try a milder register hint that does not target extra resident blocks | bottleneck: Compiler register allocation quality on the accepted 128x128 K16 kernel.
- dir_03: Hold the accepted base fixed and use the deferred L2-friendly block-order clue as the next orthogonal axis | bottleneck: Inter-CTA cache reuse rather than within-CTA feed or occupancy.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
