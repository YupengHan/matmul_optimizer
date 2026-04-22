# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 1/20` with `20` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_175153`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/20 maps the persistent guidance explicitly: register reuse stays primary, tiling stays alive but deferred, and deeper async-copy staging is deferred because the staged 128x128 family already regressed while the current run is still first-order register/occupancy bound.`
- dir_01: Swap The Recovered PTX Hot-Band Back To The Regular 128x128 Single-K Sibling | bottleneck: Microkernel-specific consume ordering and residual accumulator live range on the dominant 128x128 hot-band path are still holding occupancy to the 2-CTA class.
- dir_02: Retune The PTX Hot-Band Launch Bounds For Three-CTA Residency | bottleneck: Register-pressure-driven CTA residency cap on the current PTX hot-band microkernel.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Family After The PTX Recovery | bottleneck: Hot-band tiling and panel-reuse ceiling on the current 128x128 surface rather than pure bandwidth or tail overhead.

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
