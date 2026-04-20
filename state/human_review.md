# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 18/50` with `33` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_000002`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 18: the primary accepted family is now Tiling, specifically the user-requested 256x128 block with 64x64 warp tiles, because the corrected 128x128 K16 path proved the base pipeline while the deeper 128x128x32 path hurt active warps. Async Copy, Pg2s, Ps2r, and Data Reuse remain accepted supporting mechanisms because the fixed hot-band kernels already rely on them and the next experiment should preserve that machinery. Coalescing Access and Bank Conflict are deferred because the current regressions are not showing mio- or bank-dominated signatures. Register Reuse is deferred because the latest failure mode was lower active warps rather than obvious fragment residency waste. The L2 cache / block-order clue remains deferred until the best CTA shape is established.`
- dir_01: Try the 256x128 hot-band CTA with 64x64 warp tiles on top of the proven K16 stage contract | bottleneck: CTA shape and active-warps pressure in the hot-band kernel, not deeper staging. The target is to improve warp residency and tensor issue while retaining the already-correct async-copy pipeline.
- dir_02: Keep 128x128 K16 as the base and narrow the new consume fence only at the stage handoff | bottleneck: Barrier overhead within the accepted 128x128 K16 hot-band loop.
- dir_03: Reserve the L2-friendly block-order clue for after the hot-band CTA shape stabilizes | bottleneck: Inter-CTA cache reuse rather than within-CTA tensor feed.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
