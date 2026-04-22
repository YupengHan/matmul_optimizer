# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 17/20` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_193904`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17/20 diagnosis emitted from the failed existing 128x128x32 staged-kernel probe; frontier should restore the accepted compact PTX anchor before any further search.`
- dir_01: Restore The Accepted Compact PTX Anchor After The Failed Existing X32 Probe | bottleneck: The immediate bottleneck is not an unresolved compact-surface seam; it is the residency and sync damage introduced by the x32 staged probe.
- dir_02: Reopen Compact Barrier Trims Only After The Anchor Is Back | bottleneck: Residual barrier overhead on the compact PTX surface after the broken x32 branch is removed.
- dir_03: Only Revisit X32 Staging If Its Register And Shared-Memory Footprint Is Cut Materially | bottleneck: Occupancy and latency hiding would remain the dominant failure mode unless the staged kernel's resident footprint is reduced substantially.

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
