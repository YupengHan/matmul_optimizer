# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 21/100` with `80` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_003952`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 21 treats round 20 as a hard negative on the exact 256x128 pivot promotion, not as a reason to retreat into more PTX-local noise chasing. The new ranking therefore promotes the closest evidence-backed alternate surface, keeps the exact PTX restore as the low-risk recovery fallback, and rehydrates one historical high-ceiling half-panel family back into the live queue so the search does not stay trapped inside 24.16-24.18 ms micro-variance.`
- dir_01: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: PTX-microkernel-specific control/export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: The round-20 regression is dominated by the bad 256x128 pivot surface itself, so the restore attacks source drift rather than a live machine bottleneck family.
- dir_03: Repair The 256x128 Half-Panel Register-Reuse Branch With Compact B Staging | bottleneck: Register-limited occupancy and oversized live state on the wide hot-band family, with the real fix requiring end-to-end half-panel staging rather than only half-width accumulation.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
