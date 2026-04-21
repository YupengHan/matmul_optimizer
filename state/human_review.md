# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/10` with `8` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_152228_round03_clean_2fbb368d`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 explicitly folds master heuristic-history families into the ranking. The just-measured non-microkernel sibling is treated as partial positive signal, not a new base: it improved the previous regressed run but still did not reclaim the clean accepted runtime. Persistent human guidance from state/human_guidance.md is now part of every frontier-search read set.`
- dir_01: Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop | bottleneck: Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are still diluting tensor issue on a latency-limited path.
- dir_02: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel is still interrupting the steady-state issue flow even on the smaller shared-memory footprint.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path are still capping residency and latency hiding on the current workload.

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
