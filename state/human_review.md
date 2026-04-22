# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/1` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_171314`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-guidance audit for this round: keep Register Reuse as the primary family, but reject the just-measured `col_step_interleaved` subfamily because the live run contradicts its design claim. Keep Async Copy / Pg2s / Stage accepted as the secondary family on the same 128x128 PTX surface, and keep 256x128 Tiling / Data Reuse alive only as the high-ceiling reopen once the current localized regression has been unwound.`
- dir_01: Replace The Failed Interleaved PTX 64x64 Hot-Band Microkernel With The Compact Row-Pair Path | bottleneck: Register-pressure-driven occupancy collapse on the dominant hot-band PTX kernel: 241 registers/thread keeps the kernel at 2 CTAs/SM and leaves tensor utilization low despite unsaturated memory bandwidth.
- dir_02: Port The PTX Hot-Band Path To The Existing 2-K Pg2s Stage Schedule | bottleneck: Wait-group, barrier, and refill cadence on the dominant hot-band path rather than raw global-memory bandwidth.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling For The Dominant Surface | bottleneck: Hot-band tiling and panel-reuse ceiling: the 128x128 hot-band surface is doing too much coordination per useful math tile and leaves too much work on the slowest profiled kernel.

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
