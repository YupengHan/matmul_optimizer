# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `node_c_context_ready`
- round loop: `round 2/20` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_175735`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 treats the regular 128x128 sibling as a measured_loss for accepted-base promotion: it improved occupancy and long-scoreboard locally, but the barrier / short-scoreboard regression dominated total runtime. The next moves all restore the compact PTX surface first and then change one lever at a time.`
- dir_01: Restore The Compact PTX Hot-Band And Retest Three-CTA Residency There | bottleneck: The accepted compact PTX surface is still register-limited, but the beneficial part of the current regression may be the 3-CTA residency rather than the sibling kernel body.
- dir_02: Restore The Compact PTX Hot-Band And Trim Barrier Cadence Without Shared-Memory Blowup | bottleneck: Single-K barrier cadence and CTA handoff overhead on the accepted compact PTX hot-band surface remain the unresolved latency tax once the row-pair live-range reset is in place.
- dir_03: Restore The Compact PTX Hot-Band And Try Grouped Rows Equals Two | bottleneck: The accepted PTX grouped-row traversal may still be mismatched to the A/B locality balance on the fixed hot-band surface.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use select-next for frontier-only loop execution.`

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
