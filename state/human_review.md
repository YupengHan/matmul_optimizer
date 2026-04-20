# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/17` with `16` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_154514`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/17 diagnosis for run 20260420_154403_bf16_gemm_v1_153bda2. Human-review mapping: accept only narrow PTX-adjacent follow-ups on top of the accepted PTX baseline; defer pure baseline-restore work because the supervisor already restored the implementation surface to c550d7959d2a7f80c98ebb0a632629ff9d196656 after this regressed round; reject reopening broad default-promotion, staged K32, paired export-lifetime, helper-flattening, and now also the x-major traversal variant from round 1/17. The round-1 experiment proved traversal was the wrong next lever: it lowered long-scoreboard from 7.79 to 4.62, but runtime regressed by 1.215487 ms because DRAM ballooned from 11.52 to 34.29. That makes export-helper cleanup the best next move, with PTX prefetch retiming and B-shared skew as the two secondary families.`
- dir_01: Trim PTX Export Syncs Inside The Single-Stage Scratch | bottleneck: PTX export-side synchronization and shared-to-global store orchestration in the hot-band epilogue.
- dir_02: Retune PTX Prefetch Handoff In The K Loop | bottleneck: Copy-pipeline handoff timing inside the PTX hot-band steady-state loop.
- dir_03: Tune PTX Hot-Band B-Shared Skew Without Touching Traversal | bottleneck: Shared-memory layout and fragment address generation for PTX hot-band B loads.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
