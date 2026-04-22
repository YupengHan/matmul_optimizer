# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 12/20` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_191808`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/20 diagnosis emitted from the measured 256x128 loss; frontier should restore the compact 128x128 PTX anchor before spending another round on a new structural probe.`
- dir_01: Restore The Compact 128x128 PTX Grouped-Rows-4 Anchor After The Failed 256x128 Reopen | bottleneck: The immediate problem is the bad 256x128 hot-band geometry itself, which inflated shared-memory footprint and collapsed tensor throughput.
- dir_02: Reopen Pairwise Wait-Sync Collapse Once The Compact PTX Anchor Is Restored | bottleneck: On the restored compact PTX surface, the remaining bottleneck is still hot-loop wait/sync cadence and latency hiding rather than tile geometry.
- dir_03: Retry The 2-K-Stage Pg2s Port Only After The Compact Anchor Is Back | bottleneck: If revisited later, the target bottleneck is compact-surface latency hiding and per-tile copy cadence, not wide-tile geometry.

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
