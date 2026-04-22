# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 13/20` with `8` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_192105`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/20 diagnosis emitted from the restored compact PTX anchor; frontier should now prefer compact-surface sync experiments over any new geometry branch.`
- dir_01: Collapse The Compact PTX Wait-Sync Seam Into A Pairwise Stage Advance | bottleneck: Barrier and long-scoreboard are the clearest remaining compact-surface bottlenecks on the restored anchor.
- dir_02: Trim The Compact PTX Wait Group And Sync Cadence Without Growing Shared Memory | bottleneck: Barrier handoff overhead is still large enough to justify a smaller cadence-only probe on the compact PTX surface.
- dir_03: Keep The 2-K-Stage Pg2s Port Parked Behind The Compact Sync Experiments | bottleneck: If revisited later, the target is still compact-surface latency hiding and copy cadence, not a new geometry surface.

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
