# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/17` with `15` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_154908`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/17 diagnosis for run 20260420_154827_bf16_gemm_v1_7adfc4e. Human-review mapping: continue to accept only narrow PTX-adjacent ideas on the recovered baseline; keep broad default-promotion, staged K32, paired export-lifetime, helper-flattening-without-locality-awareness, and x-major traversal closed. The key update is that the export-helper family is now confirmed live: the bounded row-pair specialization improved runtime to 25.50532818 ms while holding DRAM at 11.54 and reducing long-scoreboard to 7.21. That makes a final TileRow flattening pass the best next move, with PTX prefetch retiming and B-shared skew as the two backup families.`
- dir_01: Finish Flattening PTX Export Across Tile Rows | bottleneck: Residual PTX export-side control overhead and per-row epilogue orchestration inside the hot-band microkernel.
- dir_02: Retune PTX Prefetch Handoff After The Export Cleanup | bottleneck: Copy-pipeline handoff timing in the PTX hot-band steady-state loop.
- dir_03: Tune PTX Hot-Band B-Shared Skew On Top Of The New Base | bottleneck: Shared-memory fragment address generation and B-tile layout friction in the PTX hot-band path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
