# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 27/100` with `74` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_011652`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 27 interprets the non-PTX sibling as a correct plateau alternate, not as a new leader. The ranking therefore re-centers the exact PTX winner while keeping the sibling and grouped_rows=8 surfaces alive as lower-ranked alternate states.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the best measured correct surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the exact same surface restore targeted by dir_01.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
