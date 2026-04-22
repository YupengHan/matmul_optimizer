# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 6/20` with `15` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_184151`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6 treats the grouped_rows=2 probe as a negative result on top of a still-informative 3-stage family. The next move should either fix the late drain or restore the clean two-stage PTX anchor before another broad branch jump.`
- dir_01: Split The Final 3-Stage PTX Drain Out Of The Late Steady-State Loop | bottleneck: Late-drain synchronization is now the clearest remaining local tax on the 3-stage PTX surface.
- dir_02: Restore The Two-Stage PTX Anchor After The 3-Stage Probes | bottleneck: This is a fallback restore family, not a new bottleneck theory: it resets the search to the cleanest recent PTX anchor so later branches can be tested from a lower-variance surface.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling On The Dominant Surface | bottleneck: The 128x128 PTX surface may still be hitting a real tiling and warp-reuse ceiling even after local pipeline cleanup.

## Active direction

- selected direction: `dir_01`
- selection mode: `frontier`
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
