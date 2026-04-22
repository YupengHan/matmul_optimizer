# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 11/20` with `10` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_191121`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/20 diagnosis emitted from the live 24.689153 ms compact PTX plateau; frontier should prefer a structural branch over stale restore-base replay.`
- dir_01: Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Current Compact PTX Base | bottleneck: The dominant ceiling is occupancy and hot-band geometry on the active 128x128 PTX path, not raw DRAM bandwidth.
- dir_02: Port The 2-K-Stage Pg2s Schedule Onto The Active 128x128 PTX Microkernel | bottleneck: The active PTX hot-band path is still limited by per-tile Pg2s cadence and the resulting latency-hiding gap.
- dir_03: Reopen Pairwise Wait-Sync Collapse On The Current Compact PTX Surface | bottleneck: The remaining bottleneck on the compact PTX surface is hot-loop synchronization cadence rather than address setup.

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
