# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 15/50` with `36` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_233204`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/50 keeps the new 128x128 family alive because it delivered the first major kernel-time improvement in many rounds. The recommended next move is a localization step: preserve the winning CTA/launch shape and revert only the K32 mainloop to K16 so the correctness bug can be isolated without discarding the structural gain.`
- dir_01: Keep the 128x128/128-thread hot-band branch but revert only the K32 mainloop back to proven K16 staging to localize correctness | bottleneck: Correctness bug likely in the K32 staged mainloop bookkeeping, not in the new 128x128 warp mapping.
- dir_02: If 128x128 K16 is correct, reintroduce K32 with explicit [stage][half] helpers to eliminate half-stage aliasing | bottleneck: Stage-half address aliasing or refill ordering inside the new K32 mainloop.
- dir_03: Restore the accepted-correct implementation surface if the new family cannot be made correct quickly | bottleneck: Not a bottleneck attack; this is the fallback path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
