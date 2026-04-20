# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/50` with `46` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_225521`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/50 starts from an incorrect but materially faster steady-state peel: the main 256x128 hot-band kernel improved by roughly 0.7 ms and tensor activity rose, but all correctness cases failed. That makes dir_01 the clear recommendation: preserve the peeled steady-state core and repair correctness by restoring the original final-two-tile handoff. Dir_02 carries the warp-local Ps2r/register-reuse human-idea branch if the peel cannot be repaired cleanly, and dir_03 keeps the lighter L2-friendly CTA swizzle as the cache-locality branch.`
- dir_01: Keep the peeled steady state, but restore the proven final-two-tile handoff to recover correctness | bottleneck: Correctness break in the final cp.async stage handoff of the peeled hot-band schedule, not a failure of the hot-band steady-state peeling idea itself.
- dir_02: Return to the accepted-correct surface and push warp-local Ps2r plus right-left register reuse | bottleneck: Per-warp operand delivery and short-scoreboard pressure inside the 64x64 PTX hot-band microkernel.
- dir_03: Try a lighter L2-friendly logical CTA swizzle over the hot-band grid | bottleneck: Inter-CTA L2 locality across the hot-band grid rather than per-warp compute scheduling.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
