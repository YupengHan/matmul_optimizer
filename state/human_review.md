# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 8/30` with `23` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_221835`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/30 starts from a clearly negative warp-local consumer-order experiment. Reversing the mirrored 64x64 B sweep to a `Right Left Right Left` order preserved correctness but regressed runtime by about 0.46 ms, slowed the hot-band kernel to about 41.76 us, and worsened tensor active, barrier stall, short scoreboard, and `mio_throttle`. The next move should therefore restore the proven pre-sweep consumer path and spend one round on a different human-idea family. Recommended direction dir_01 does exactly that while also trying the fixed-shape stage-peeling idea on the hot-band K loop. Dir_02 keeps the cp.async ownership experiment ready on the same restored surface, and dir_03 is the pure restore fallback if the peeling change grows too large.`
- dir_01: Human idea stage: restore the pre-sweep best surface and peel the hot-band K loop into steady-state | bottleneck: Fixed-shape control-flow and stage-transition overhead inside the hot-band K loop.
- dir_02: Human idea coalescing + async copy: restore the pre-sweep best surface and retune cp.async ownership | bottleneck: Global-to-shared staging issue regularity and LSU ownership balance.
- dir_03: Restore the pre-sweep best surface without adding a new experiment | bottleneck: Not a direct bottleneck attack; this is a branch repair after a negative warp-local consumer experiment.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
