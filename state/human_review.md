# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 8/10` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_155620`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 8: the current loop still respects the user's 256x128/64x64 preference, but the latest negative result is not yet a clean reason to abandon the accepted-base family. The round-7 surface carried both 3-CTA residency and a two-stage export scratch lifetime, so the first priority is to separate those effects. That is why dir_01 trims export scratch first, dir_02 keeps a same-surface barrier retime in reserve, and the 256x128 family stays queued rather than selected immediately.`
- dir_01: Trim The Grouped-Row 128x128 Sibling Export Scratch To Single Stage | bottleneck: Shared export lifetime and barrier tax on the grouped-row non-PTX 128x128 sibling, currently confounded with the 3-CTA residency probe.
- dir_02: Retime The Non-PTX 3-CTA Barrier/Handoff Seam | bottleneck: Barrier cadence at the seam between cp.async wait completion, __syncthreads(), and future-tile refill ordering on the non-PTX 3-CTA sibling.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, B-fragment lifetime, and writer-ownership constraints on the correctness-safe 256x128 pivot.

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
