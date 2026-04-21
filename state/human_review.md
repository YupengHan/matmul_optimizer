# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 30/100` with `71` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_013125`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 30 treats round 29 as a structurally useful failure. The launch-bounds probe did exactly what the occupancy diagnosis wanted: registers fell from 200 to 168, occupancy_limit_registers rose from 2 to 3, active warps rose from 16.59% to 24.77%, and long-scoreboard stall collapsed from 7.34% to 1.69%. The runtime regression therefore points to the next missing piece, not a fully wrong premise: barrier stall doubled to 10.97% and the hot-band kernel slowed from about 32.69 us to about 33.76 us. The ranking therefore continues the aggressive path, but narrows it to barrier amortization on top of the newly proven occupancy gain.`
- dir_01: Keep 3-CTA Residency And Amortize Barriers With Two-K Stages | bottleneck: Synchronization and stage handoff overhead after the residency wall has been partially relaxed.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and handoff strategy in the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
