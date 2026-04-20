# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/50` with `47` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_224955`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/50 starts from a run where the dedicated residual 64x128 PTX kernel helped the last 64 rows, but the dominant 256x128 hot-band kernel remained effectively unchanged relative to the accepted base. The recommended next move is therefore dir_01: keep the new shared 64x64 PTX family, but peel the fixed 452-tile steady state so the compiler sees an exact prologue / steady-state / epilogue schedule. Dir_02 keeps pressure inside warp-local Ps2r/register reuse, and dir_03 holds the lighter L2-swizzle idea as a lower-ranked cache-locality branch.`
- dir_01: Peel the 452-tile steady state for the shared 64x64 PTX hot-band family | bottleneck: Hot-band control/orchestration overhead inside the fixed-shape PTX main loop, which is still diluting tensor issue after the residual path was specialized.
- dir_02: Push warp-local Ps2r and register-reuse scheduling inside the 64x64 PTX microkernel | bottleneck: Per-warp operand delivery and short-scoreboard pressure inside the hot-band MMA loop rather than CTA-level shared-memory staging.
- dir_03: Try a light L2-friendly CTA swizzle over the 60x25 hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band B tiles rather than per-CTA tensor scheduling.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
