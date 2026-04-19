# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/20` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_224925`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- dir_01: Reuse one 16x16 epilogue scratch tile per warp with warp-synchronous pair stores | bottleneck: Shared-memory footprint and epilogue traffic are still constraining residency and keeping tensor utilization low after the B-tile skew fix. The current `c_shared` design stores all three output tiles per warp at once even though they are consumed strictly one tile at a time.
- dir_02: Prototype a shuffle-assisted BF16 pair-packing epilogue after each WMMA store | bottleneck: The current epilogue converts and stores each output element as a scalar BF16 write after a shared-memory round-trip, which may be amplifying short scoreboard and writeback pressure even after the main tensor loop improved.
- dir_03: Investigate a fragment-unpack path that bypasses `c_shared` entirely | bottleneck: The `c_shared` round-trip may be fundamentally unnecessary overhead once the tensor loop itself is healthy, but the current WMMA abstraction makes a direct path difficult.

## Active direction

- selected direction: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
