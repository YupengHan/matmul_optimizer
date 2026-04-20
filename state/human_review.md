# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/17` with `14` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_155107`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/17 diagnosis for run 20260420_155035_bf16_gemm_v1_a4dc968. Human-review mapping: keep broad default-promotion, staged K32, paired export-lifetime, x-major traversal, and deeper export flattening closed; continue to accept only narrow PTX-adjacent moves on top of the accepted base 20260420_154827_bf16_gemm_v1_7adfc4e at 25.50532818 ms. The round-3 result shows the export family has likely plateaued: DRAM stayed healthy at 11.52, but the extra TileRow flattening regressed runtime by 0.0404005 ms and pushed long-scoreboard back to 7.75. That makes PTX prefetch handoff the best next move, with B-shared skew as the main alternate family and only a minimal export-side cleanup retained as a low-risk control.`
- dir_01: Retune PTX Prefetch Handoff On Top Of The Accepted Export Base | bottleneck: Copy-pipeline handoff timing in the PTX hot-band steady-state loop.
- dir_02: Tune PTX Hot-Band B-Shared Skew On The New Base | bottleneck: Shared-memory fragment address generation and B-tile layout friction in the PTX hot-band path.
- dir_03: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: Residual address-generation overhead in the PTX export helper on top of the accepted one-stage scratch design.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
