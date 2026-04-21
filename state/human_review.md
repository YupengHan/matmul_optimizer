# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 24/100` with `77` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_010129`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 24 closes the immediate half-panel continuation: the branch preserved the occupancy breakthrough but failed correctness twice in a row and did not recover runtime. The next best move is to restore a correct baseline first, then choose the next aggressive family from there.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is an exact recovery of the best-known implementation surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: This is a safe alternate-surface recovery, not a new bottleneck attack.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Hot-band K-loop scheduling and latency hiding on a broader 256x128 reuse regime rather than the plateaued 128x128 surfaces.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
