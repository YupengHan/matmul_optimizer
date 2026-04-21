# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 6/10` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_154619`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 6: the 256x128 / 64x64 idea family remains strategically relevant, but the latest clean-loop evidence says it should not be the next code edit. The round-4 256x128 pivot and round-5 compact transplant both left the branch in the same losing machine state, while the cuBLASLt reference makes the ceiling clearer: this workload is not missing raw active-warps so much as it is missing a low-friction synchronization and handoff regime. That is why dir_01 ranks first even though it steps away from the currently running 256x128 surface. The queue still preserves one bounded occupancy probe on the accepted non-PTX 128x128 sibling and one deferred high-ceiling 256x128 branch so the search does not collapse back into a single-family local minimum.`
- dir_01: Trim PTX Wait/Sync Handoff On The 128x128 Anchor | bottleneck: Barrier cadence and export/control handoff inside the single-K 128x128 PTX microkernel, especially the seam between finishing a tile, releasing the stage with __syncthreads(), and refilling the reused buffer.
- dir_02: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the accepted non-PTX 128x128 hot-band surface.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, B-fragment lifetime, and writer-ownership constraints inside the 256x128 hot-band pivot.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
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
