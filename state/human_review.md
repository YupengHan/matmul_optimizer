# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 33/100` with `68` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_014129`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 33 groups the PTX and non-PTX 128x128 launch-bounds probes into one coherent negative family. Both branches reached about 168 registers, about 24.7% active warps, and about 3 CTA residency, and both regressed because barrier stall climbed to about 11%. The x32 follow-on also already showed that doubling shared memory to amortize those barriers is not acceptable. The right move now is to restore the exact PTX anchor and then spend the next aggressive budget on true barrier surgery or on the broader 256x128 low-register branch, not on another launch-bounds replay.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface, used here as a recovery anchor.
- dir_02: Trim PTX Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K PTX microkernel after the residency experiments exposed synchronization as the real limiting cost.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 path, plus correctness-sensitive writer ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
