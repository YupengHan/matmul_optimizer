# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 10/10` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_160315`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 10: the 256x128 branch remains the strategic high-ceiling family, but the accepted-base family already produced enough evidence that the final round is better spent on one last bounded near-base PTX synchronization probe. The non-PTX 3-CTA family is now sufficiently tested and should be treated as closed after this loop.`
- dir_01: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: Wait-group release, barrier cadence, and refill ordering on the PTX 128x128 anchor without extra export-scratch growth.
- dir_02: Reopen The 256x128 Half-Panel Register-Reuse Branch | bottleneck: Register reuse, compact B staging, and half-panel export mapping on the 256x128 pivot branch.
- dir_03: Restore The Accepted Base If The Final Probe Fails | bottleneck: None. This is a state-restoration fallback, not a new performance hypothesis.

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
