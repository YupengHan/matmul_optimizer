# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 18/100` with `83` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_002857`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 18 treats the restore family as absorbed again: the source matches the PTX winner surface and runtime has returned to the 24.17 band. The next recommendation therefore moves to the strongest alternate live family, grouped_rows=8, while 256x128 pivot and the non-PTX 128x128 sibling remain in the diagnosis to preserve queue breadth after the search-policy reset.`
- dir_01: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer-order locality on the PTX hot-band microkernel, not the already-restored prologue/refill seam on the grouped_rows=4 winner surface.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path, not the current PTX control-path seam.
- dir_03: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: CTA traversal and locality on the non-PTX 128x128 sibling surface rather than PTX microkernel control-path behavior.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
