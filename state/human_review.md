# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 7/10` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_155253`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 7: the latest run validated the choice to leave the losing 256x128 surface, but it did not validate staying on the PTX family as the main branch. The recovered PTX run became a good fallback surface, not the new winner. That is why the ranking now prefers the accepted non-PTX sibling plus one bounded occupancy probe, keeps one PTX wait/sync-collapse refinement in reserve, and leaves the 256x128 family queued rather than deleting it.`
- dir_01: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the accepted non-PTX 128x128 hot-band surface.
- dir_02: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: The seam between cp.async wait-group release, __syncthreads(), and future-stage refill ordering on the PTX 128x128 microkernel.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, fragment lifetime, and writer-ownership constraints on the correctness-safe 256x128 pivot.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
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
