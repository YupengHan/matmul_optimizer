# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 84/100` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_152858`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 84/100 diagnosis for run 20260420_120552_bf16_gemm_v1_84de30b. Human-review mapping: accept narrow PTX-adjacent ideas and very small export/feed/orchestration experiments on top of the zero-padding PTX baseline; defer pure baseline-restore work unless it isolates the current regression; reject reopening the broad default-promotion family, the staged K32 family, the paired PTX export-lifetime helper, helper flattening without a new codegen thesis, and the already-flat grouped_rows=4 replay as a standalone answer. The latest regression is confounded: the measured run tightened kFixedHotBandPtxGroupedRows from 8 to 4, but it also left the PTX hot-band microkernel family entirely and launched the regular 128x128 hot-band kernel. That only trimmed hot-band long-scoreboard slightly (7.61 -> 7.25) while blowing up hot-band DRAM throughput (10.29% -> 30.29%), so the next step should re-isolate long-scoreboard work inside the PTX path instead of ranking the current non-PTX result as the true grouped-row answer.`
- dir_01: Re-enter The PTX Hot-Band Path With A Mid-Width Grouping Control | bottleneck: Long-scoreboard in the PTX hot-band kernel, with DRAM and L2 locality acting as guardrails while the grouped-row mapping is re-isolated.
- dir_02: Retune PTX Microkernel Feed Cadence Around The Row-Pair Loop | bottleneck: Feed latency and stage handoff inside the PTX hot-band steady-state loop, showing up as long-scoreboard and barrier tradeoffs around the row-pair MMA traversal.
- dir_03: Rework PTX Group Traversal To Preserve B Locality Without Broad Groups | bottleneck: Hot-band orchestration and CTA traversal locality, especially the balance between B reuse, L2 behavior, and scoreboard cost across grouped-row boundaries.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
