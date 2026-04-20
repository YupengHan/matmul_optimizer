# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 7/50` with `44` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_230227`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/50 pivots away from peeled control-flow experiments because the main hot-band speedup is real but correctness has not recovered after multiple repair attempts. The recommended next move is therefore dir_01: restore the accepted-correct hot-band loop and test the user's warp-local right-left-right-left register-reuse idea as an isolated experiment.`
- dir_01: Restore the accepted-correct control flow and switch the 64x64 column sweep to explicit right-left-right-left order | bottleneck: Per-warp operand delivery and register reuse inside the 64x64 PTX hot-band microkernel rather than CTA-level pipeline control.
- dir_02: Keep the accepted-correct loop and deepen warp-local Ps2r with next-A-row-pair lookahead | bottleneck: Warp-local shared-to-register latency on the A-side of the 64x64 PTX microkernel.
- dir_03: Return to a light L2-friendly logical CTA swizzle once correctness is back on the accepted surface | bottleneck: Inter-CTA L2 reuse across neighboring hot-band B tiles.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
