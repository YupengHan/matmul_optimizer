# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 16/20` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_193427`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16/20 diagnosis emitted from the post-checkpoint compact anchor regression; frontier should try the existing 128x128x32 staged kernel before spending more rounds on tiny compact seam trims.`
- dir_01: Promote The Existing 128x128x32 Two-K-Stage Hot-Band Kernel From The Clean Compact Anchor | bottleneck: The unresolved bottleneck is still latency hiding and copy/sync amortization on the accepted compact surface, not a new geometry family.
- dir_02: Restore The Accepted Compact PTX Anchor If The Broader Staged Probe Loses | bottleneck: The immediate fallback problem would be a failed staged-kernel branch rather than a fresh compact-surface bottleneck.
- dir_03: Leave The Tiny Compact Sync Tweaks Parked Behind The Broader Staged Probe | bottleneck: If revisited later, the target would still be residual barrier overhead on the compact anchor, but not before the staged probe is measured.

## Active direction

- selected direction: `dir_01`
- selection mode: `frontier`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

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
