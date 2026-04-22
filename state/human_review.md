# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/20` with `18` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_182251`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 treats 49dfa799 as a local launch-policy regression on top of the compact PTX base, not as a reason to abandon the PTX hot-band family. The next move should isolate launch_bounds before reopening larger geometry or shared-memory families.`
- dir_01: Restore PTX Launch Bounds Back To 2-CTA On The Active Hot-Band Path | bottleneck: The explicit 3-CTA minimum is over-constraining the PTX microkernel schedule, inflating barrier and short-scoreboard even though it does not reduce the measured register footprint.
- dir_02: Split The Final PTX Wait/Sync Drain Out Of The Steady-State Loop | bottleneck: The final steady-state handoff is paying an unnecessary wait/sync pair that shows up as barrier and short-scoreboard tax on the PTX path.
- dir_03: Retune PTX Hot-Band Grouped Rows From 4 Down To 2 | bottleneck: PTX grouped-row batching may be over-amortizing locality and paying too much synchronization and scheduler delay per group.

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
