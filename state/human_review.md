# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 23/100` with `78` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_005735`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 23 interprets the half-panel result as partial signal, not a total miss. The branch remained wrong and too slow, but it reproduced the historical occupancy breakthrough on the current environment. That justifies one final targeted continuation before mechanically restoring to a plateau surface.`
- dir_01: Single-Source Warp Ownership End To End On The Half-Panel Branch | bottleneck: Half-panel ownership and export correctness on top of a branch that already solved the live-state wall but still pays excessive synchronization.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked; this is an exact recovery of the best-known implementation surface.
- dir_03: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: This is a safe alternate-surface recovery, not a new bottleneck attack.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
