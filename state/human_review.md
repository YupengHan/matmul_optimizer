# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 10/20` with `11` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_190245`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10 diagnosis emitted after the barrier-trim experiment regressed and should be cleared before the checkpoint.`
- dir_01: Restore The Accepted Compact PTX Cadence After The Failed Barrier Trim | bottleneck: This is a recovery direction rather than a new bottleneck theory; its purpose is to remove a falsified sync variant and return to the accepted compact PTX surface.
- dir_02: Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Accepted PTX Base | bottleneck: The 128x128 PTX surface may still be constrained by geometry and warp-reuse limits once the local cadence is back on the accepted base.
- dir_03: Port The PTX Hot-Band Path To The Existing 2-K Pg2s Stage Schedule | bottleneck: Barrier, refill cadence, and latency hiding on the dominant hot-band path rather than raw DRAM bandwidth.

## Active direction

- selected direction: `dir_02`
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
