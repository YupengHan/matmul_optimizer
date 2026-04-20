# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/50` with `42` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_230713`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/50 resumes forward optimization from a restored correct surface. The recommended next move is dir_01, which follows the human Ps2r idea on the A side while keeping control flow and CTA staging unchanged so the result stays easy to interpret.`
- dir_01: Keep the restored control flow and add A-side row-pair lookahead inside the 64x64 PTX microkernel | bottleneck: Warp-local shared-to-register latency on the A-fragment path inside the 64x64 PTX microkernel.
- dir_02: Keep the restored surface and test a light L2-friendly logical CTA swizzle | bottleneck: Inter-CTA L2 reuse across neighboring hot-band B tiles.
- dir_03: Try warp-specialized Pg2s staging on the restored surface without changing the tile shape | bottleneck: CTA-level staging orchestration and barrier dilution inside the hot-band loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
