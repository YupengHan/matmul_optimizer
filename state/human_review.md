# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/50` with `43` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_230527`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/50 resets the search: the current correct branch is materially slower than the accepted best implementation, and several recent rounds have mixed correctness/debug work with forward optimization. The recommended next move is therefore dir_01, a clean restore to commit 0d78758. Dir_02 and dir_03 then capture the next two human-idea branches to try on that restored surface: deeper A-side Ps2r and a lighter L2-friendly CTA swizzle.`
- dir_01: Re-anchor exactly at the accepted best implementation commit 0d78758 before more experiments | bottleneck: Not a bottleneck attack. This is a reset to the fastest correct implementation surface before the next human-idea experiments.
- dir_02: On the restored surface, try A-side Ps2r row-pair lookahead inside the 64x64 PTX microkernel | bottleneck: Warp-local shared-to-register latency on the A-side of the 64x64 PTX hot-band microkernel.
- dir_03: On the restored surface, test a light L2-friendly logical CTA swizzle on the hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band tiles.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
