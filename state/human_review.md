# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 7/20` with `14` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_184831`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7 diagnosis emitted from live reasoning after the round-6 drain-split regression.`
- dir_01: Restore A Compact Two-Stage PTX Ring While Keeping Grouped Rows At 2 | bottleneck: Registers-per-thread and occupancy are the first bottlenecks to remove; barrier cleanup is no longer the primary limiter after the round-6 regression.
- dir_02: Restore The Known Two-Stage PTX Anchor With Grouped Rows Back At 4 | bottleneck: This is a restore family aimed at removing register and occupancy damage rather than discovering a new local bottleneck.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Branch After Resetting Register Pressure | bottleneck: The 128x128 PTX surface may still be capped by geometry and warp-reuse limits even after register cleanup.

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
