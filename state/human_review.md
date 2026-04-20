# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 11/50` with `40` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_231228`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/50 moves from the flat L2 swizzle to the next human-idea family: Pg2s orchestration. The recommended next move is dir_01, a conservative half-CTA staging subset that keeps tile shape, control flow, and the consumer microkernel intact while reducing the number of threads issuing async copies in the hot-band kernel.`
- dir_01: Keep the restored correct surface and let only half the CTA issue hot-band Pg2s async copies | bottleneck: CTA-level staging orchestration and LSU/shared issue pressure during Pg2s rather than warp-local MMA scheduling.
- dir_02: Keep the restored surface and try a light consumer-side B XOR swizzle instead of extra padding | bottleneck: Shared-memory bank behavior on the B operand path without adding CTA-level repacking.
- dir_03: Restore-only fallback to the accepted-correct surface | bottleneck: Not a bottleneck attack; this is the reset path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
