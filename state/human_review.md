# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 28/100` with `73` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_012002`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 28 explicitly treats both the exact PTX winner and the non-PTX sibling as plateau anchors. The main search budget shifts to one clean recheck of grouped_rows=8 so the loop can either validate or close that alternate PTX surface with fresh evidence.`
- dir_01: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the already-replayed exact PTX restore and not another same-plateau alternate-surface A/B.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the strongest measured anchor.
- dir_03: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
