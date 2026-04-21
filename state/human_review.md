# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 5/10` with `6` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_153357_round05_clean_f1c576ee`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5 human-guidance review: Tiling(accept but reject simple 256x128 promotion), Coalescing Access(guardrail, already present), Data Reuse(accept), Async Copy(guardrail, already present), Bank Conflict(accept), L2 Cache(accept as secondary), Register Reuse(strong accept), Pg2s(accept), Ps2r(accept), Stage(accept but reject shared-memory blowup). The simple 256x128 pivot is now treated as a measured negative; only deeper 256x128 salvage or bounded occupancy probes stay active.`
- dir_01: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint, stage design, and reuse efficiency inside the 256x128 hot-band path are still the missing pieces preventing the human-guided tiling family from becoming viable.
- dir_02: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the current non-PTX 128x128 accepted surface.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the lower shared-memory footprint.

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
