# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/5` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_212050`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Restore explicit cp.async warm-up and consume ordering | bottleneck: Correctness-breaking cp.async producer/consumer hazard in the ping-pong pipeline; after recovery, the remaining limit is still CTA synchronization and MIO throttle rather than DRAM saturation.
- dir_02: Fall back to a correctness-first single-stage staging path | bottleneck: Synchronization and MIO throttle overhead from an over-complicated copy pipeline, not raw memory bandwidth. The current profile already shows barrier stalls rising to 23.82% and MIO throttle to 39.04% while performance regresses.
- dir_03: Amortize sync with a two-slice K macro-stage | bottleneck: Barrier and MIO throttle from too-frequent 16-wide stage turnover, which leaves tensor utilization low at 13.46% even though active warps stay high.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
