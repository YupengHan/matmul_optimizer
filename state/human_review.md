# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 29/50` with `22` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002345`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 29: Stage is promoted again, but specifically as a re-evaluation of the K32 branch under the new grouped-order plus compiler-guided base. The earlier K32 rejection remains valid for the old regime, but the current best branch changed the occupancy/codegen picture enough that the comparison should be refreshed once. Register Reuse and L2 Cache remain accepted because the current best branch already depends on both. Tiling 256x128, aggressive launch-bounds, and the peeled schedule remain rejected.`
- dir_01: Revisit the 128x128x32 hot-band branch on top of the current grouped-order plus launch-bounds base | bottleneck: Stage-depth / control-overhead tradeoff under the new best branch conditions, not under the older pre-grouped baseline.
- dir_02: Keep the current best K16 branch fixed and revisit tiny barrier-side cleanup only if the K32 re-test fails again | bottleneck: Residual barrier overhead in the grouped-order plus launch-bounds K16 winner.
- dir_03: Freeze the current best hot-band branch and look at a small secondary-region optimization only after the K32 re-test result is known | bottleneck: Secondary-region overhead outside the main hot band.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
