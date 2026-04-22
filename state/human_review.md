# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/20` with `13` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_185158`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8 diagnosis emitted after the compact two-stage grouped_rows=2 retest recovered registers but reintroduced a large long_scoreboard penalty.`
- dir_01: Restore Grouped Rows From 2 Back To 4 On The Compact Two-Stage PTX Ring | bottleneck: Long-scoreboard pressure from the grouped_rows=2 launch order is now the most specific local bottleneck to remove.
- dir_02: Trim The Compact Two-Stage PTX Wait-Sync Cadence Without Growing Shared Memory | bottleneck: Barrier and CTA handoff overhead are the likely next bottlenecks after grouped_rows is restored.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Branch From The Compact PTX Base | bottleneck: The 128x128 PTX surface may still be occupancy-limited by geometry and warp reuse even after local launch-order cleanup.

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
