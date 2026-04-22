# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 15/20` with `6` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_193031`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/20 diagnosis emitted from the current accepted compact PTX base; frontier should try the smallest final-drain barrier trim before the checkpoint.`
- dir_01: Skip The Final No-Refill CTA Sync On The Compact PTX Anchor | bottleneck: The remaining local tax is unnecessary final-drain barrier overhead on the accepted compact PTX surface.
- dir_02: Keep The Guarded 2-K-Stage Pg2s Port As The Broader Fallback | bottleneck: If revisited later, the target remains compact-surface latency hiding and per-tile copy cadence.
- dir_03: Leave The Wait-Sync-Collapse Family Parked Behind Smaller Compact Tweaks | bottleneck: If revisited later, the target would again be the compact loop's wait/refill seam, but not before smaller barrier trims flatten out.

## Active direction

- selected direction: `dir_01`
- selection mode: `frontier`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Persistent human guidance

Read these items on every frontier-search / node_b ranking pass and map them into `family_audit`, diagnosis notes, or direction ranking when relevant.

- `Tiling`: `256 x 128` for block tiling size and `64 x 64` for warp tiling size
- `Coalescing Access`: use wide-instruction access to global memory
- `Data Reuse`: use shared memory to reuse data from matrix `A` and matrix `B`
- `Async Copy`: use asynchronous copy operations with non-blocking instructions
- `Bank Conflict`: use padding for the WMMA API and a permuted layout for MMA PTX instructions to eliminate bank conflicts
- `L2 Cache`: use swizzle access mode to increase the L2 cache hit ratio
- `Register Reuse`: calculate the internal warp tile as `Right Left Right Left`
- `Pg2s`: use a double-buffer algorithm that prefetches global memory into shared memory
- `Ps2r`: use a double-buffer algorithm that prefetches shared memory into registers
- `Stage`: use a multi-buffer algorithm that prefetches global memory into shared memory
