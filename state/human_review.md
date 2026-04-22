# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 14/20` with `7` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_192742`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/20 diagnosis emitted from a second compact-surface wait_sync_collapse loss; frontier should restore the clean compact seam before trying another family.`
- dir_01: Restore The Compact Two-Stage PTX Anchor After The Failed Wait-Sync-Collapse Variant | bottleneck: The immediate problem is the regressing wait_sync_collapse variant itself, which raised barrier and registers on the active compact surface.
- dir_02: Retry The Narrow Compact PTX Cadence Trim After Restoring The Anchor | bottleneck: Barrier remains the clearest unresolved compact-surface stall once the failed wait_sync_collapse variant is unwound.
- dir_03: Keep The Guarded 2-K-Stage Pg2s Port As The Third Compact-Anchor Fallback | bottleneck: If revisited later, the target remains latency hiding on the compact PTX surface rather than another wide-tiling change.

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
