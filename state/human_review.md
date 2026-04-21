# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 17/100` with `84` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_002435`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17 explicitly treats the latest PTX wait-window retime as negative evidence. The current source no longer matches the best measured PTX surface: it differs by the round-15 future_tile_k hoist and the round-16 prologue wait retime, and the latter pushed runtime back up to 24.190864 ms. The immediate recommendation is therefore a direct PTX-surface restore, while grouped_rows=8 and the 256x128 pivot branch remain live because the user asked to repopulate promising round_history families into the active search queue.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the proven PTX winner surface, specifically the prologue wait window and refill-address hot-band seam, not a need for another fresh PTX control experiment on top of the regressed variant.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer locality in the PTX hot-band microkernel, not the same prologue wait seam that just regressed.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path rather than another narrow PTX wait/commit change.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
