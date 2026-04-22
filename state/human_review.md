# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `single-run` with `0` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_163733`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for the current round: registers/thread jumped 34 after the round-10 wait-group collapse, collapsing occupancy to 2 CTAs/SM and regressing long_scoreboard and mio_throttle. The dominant lever is therefore Register Reuse on the existing PTX microkernel (dir_01), which maps the measured evidence onto the Right-Left-Right-Left warp tile guidance. Async Copy / Pg2s / Stage is kept alive on the same surface via dir_02 (3-stage cp.async pipeline) as the latency-hiding complement. The 256x128 Tiling branch remains the high-ceiling future move but is held at rank 3 because two previous reopens regressed; it should only be taken when dir_01 is exhausted or fails.`
- dir_01: Trim PTX 64x64 Microkernel Register Footprint Back To 3-CTA Class | bottleneck: Register-pressure-bound occupancy: 202 regs/thread caps SM residency at 2 CTAs, starving the long_scoreboard / mio_throttle latency hiding budget at 16.58% active warps.
- dir_02: Deepen PTX 128x128 Async Copy Pipeline To A 3-Stage Pg2s Buffer | bottleneck: Global-to-shared latency hiding at low occupancy: long_scoreboard 5.53 (+3.26 vs prev) and mio_throttle 4.0 (+2.23 vs prev) indicate warps are stalling on cp.async completion instead of making tensor-pipe progress.
- dir_03: Reopen 256x128 Half-Panel Register-Reuse Tiling Branch | bottleneck: Tile-granularity / register-reuse ceiling: at 128x128 the A panel is reloaded for every 128 columns; a 256x128 panel doubles A reuse per cp.async batch while keeping B staging compact.

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
