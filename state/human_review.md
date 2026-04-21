# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/10` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_160019`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 9: the current accepted-base family has now cleanly isolated the synchronization problem. That means the right next move is not another occupancy or export-lifetime theory; it is one final barrier/handoff retime on the current non-PTX 3-CTA surface. If that fails, the family should be closed and the final round can move to the broader 256x128 branch.`
- dir_01: Retime The Non-PTX 3-CTA Barrier/Handoff Seam | bottleneck: Barrier cadence and future-tile refill ordering on the non-PTX 3-CTA grouped-row hot-band kernel.
- dir_02: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: Wait-group release, barrier cadence, and refill ordering on the PTX 128x128 anchor without extra scratch growth.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, fragment lifetime, and writer-ownership constraints on the correctness-safe 256x128 pivot.

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
