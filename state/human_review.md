# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 26/100` with `75` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_011427`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 26 treats round 25 as a clear negative on the auxiliary 256x128 structural probe. The ranking now returns to correctness-proven alternate surfaces rather than spending another round on a closed geometry family or a frozen PTX micro-retime family.`
- dir_01: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the best measured correct surface.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the same surface restore targeted by dir_02.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
