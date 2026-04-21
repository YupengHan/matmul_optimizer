# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 32/100` with `69` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_013852`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 32 starts from a recovered clean base, so the ranking can go back to fully aggressive directions instead of spending a slot on recovery. The key evidence from the last three rounds is now coherent: the accepted PTX anchor remains around 24.17 ms at 200 registers and about 16.6% active warps; the PTX launch-bounds probe proved that lower-register 3-CTA residency can move the machine state but suffered a barrier blowup; the x32 follow-on proved that barrier amortization cannot come from doubling shared memory to 43 KB. The next bounded aggressive probe should therefore test the same occupancy thesis on the correctness-proven non-PTX 128x128 sibling before reopening broader or more manual branches.`
- dir_01: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the non-PTX 128x128 sibling surface.
- dir_02: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the small shared-memory footprint.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
