# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 19/100` with `82` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_003229`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19 treats grouped_rows=8 as clear negative evidence. The next move is a direct restore back to the PTX winner surface, while 256x128 pivot and the non-PTX 128x128 sibling remain live as the next two alternate families.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: The grouped_rows=8 locality regime itself is the measured problem here; the immediate need is to remove that drift and recover the proven PTX winner surface.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path rather than PTX grouped-row locality.
- dir_03: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: CTA traversal and locality on the non-PTX 128x128 sibling surface rather than PTX microkernel control behavior.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
