# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 4/10` with `7` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_153021_round04_clean_24f31aab`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4 explicitly lets the persistent human guidance pull the ranking toward 256x128 families. The round-3 hoist win is accepted as a useful 128x128 cleanup, but it did not move occupancy or scoreboard enough to justify another small 128x128-only exploit first.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Current four-warp 128x128 CTA geometry is capping residency and CTA-count efficiency on the hot-band region more than local pointer arithmetic is.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path are still capping residency and latency hiding.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence and PTX-stage handoff overhead inside the single-K 128x128 microkernel remain an unresolved latency tax on the accepted PTX surface.

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
