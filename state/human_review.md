# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/100` with `99` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_110945`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 diagnosis prioritizes recovery after the 256x128 probe regressed badly while only partially solving the original register hotspot.`
- dir_01: Restore the accepted PTX hot-band anchor and discard the failed 256x128 probe | bottleneck: Recovery to the known PTX plateau before any further latency-hiding or barrier experiment is attempted
- dir_02: Recover the PTX baseline, then trim live control state before retrying geometry | bottleneck: occupancy_latency_hiding_issue on the accepted PTX hot-band path, with barrier as a secondary seam
- dir_03: If 256x128 is revisited, pivot from register shaving to barrier and short-scoreboard cleanup | bottleneck: synchronization_barrier_issue and short_scoreboard pressure inside the 256x128 pivot after the register budget has already been reduced

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
