# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 23/50` with `28` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_001328`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 23: L2 Cache remains primary because grouped_rows=8 produced a real improvement and grouped_rows=16 provided useful negative evidence, which means this axis is still actively informative. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted fixed infrastructure under the current base. Register Reuse remains deferred after the launch-bounds failure. Tiling 256x128 stays rejected. Coalescing Access and Bank Conflict remain deferred because the current wins and losses are still tracking CTA-order choices more than those signals.`
- dir_01: Keep the grouped CTA-order remap and reduce the hot-band row-group size to check the other side of the L2 curve | bottleneck: Cross-CTA cache locality on the accepted grouped-order hot-band kernel.
- dir_02: Hold grouped_rows=8 as the accepted L2 base and return to conservative K16 barrier-side cleanup | bottleneck: Residual barrier overhead in the accepted grouped-order K16 kernel.
- dir_03: Freeze the accepted grouped-order kernel and revisit a strictly milder register hint later | bottleneck: Compiler allocation quality on top of the accepted grouped-order base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
