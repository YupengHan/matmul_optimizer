# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 24/50` with `27` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001453`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 24: L2 Cache has now produced the best measured branch and `grouped_rows=8` appears to be the best tested setting, so the next step is to keep that gain and combine it with the mildest plausible compiler clue from the Register Reuse family. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background infrastructure. Tiling 256x128 stays rejected. Aggressive launch-bounds remains rejected, but a single-argument launch-bounds hint is materially different and lower risk. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Restore grouped_rows=8 and try a single-argument launch-bounds clue on the accepted hot-band kernel | bottleneck: Compiler allocation / scheduling quality on top of the accepted grouped-order 128x128 K16 kernel.
- dir_02: Accept grouped_rows=8 as fixed and return to conservative K16 barrier cleanup | bottleneck: Residual barrier overhead in the accepted grouped-order K16 kernel.
- dir_03: Keep the grouped_rows=8 base and test one intermediate grouped-order value only if compiler and stage tweaks stall | bottleneck: Fine-grained cache-locality tuning around the accepted grouped-order base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
