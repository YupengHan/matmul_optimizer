# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `153bda22f3d30b70b379e1ed0362d78c9f57f3f3`
- plateau counter: `27`
- round loop: `round 2/17`
- rounds remaining: `16`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 2/17.`

## Latest measured custom run

- run id: `20260420_154403_bf16_gemm_v1_153bda2`
- run dir: `runs/20260420_154403_bf16_gemm_v1_153bda2`
- correctness: `PASS`
- median runtime: `26.978816 ms`
- TFLOP/s: `26.947788 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_154514`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/17 diagnosis for run 20260420_154403_bf16_gemm_v1_153bda2. Human-review mapping: accept only narrow PTX-adjacent follow-ups on top of the accepted PTX baseline; defer pure baseline-restore work because the supervisor already restored the implementation surface to c550d7959d2a7f80c98ebb0a632629ff9d196656 after this regressed round; reject reopening broad default-promotion, staged K32, paired export-lifetime, helper-flattening, and now also the x-major traversal variant from round 1/17. The round-1 experiment proved traversal was the wrong next lever: it lowered long-scoreboard from 7.79 to 4.62, but runtime regressed by 1.215487 ms because DRAM ballooned from 11.52 to 34.29. That makes export-helper cleanup the best next move, with PTX prefetch retiming and B-shared skew as the two secondary families.`
- dir_01: Trim PTX Export Syncs Inside The Single-Stage Scratch | bottleneck: PTX export-side synchronization and shared-to-global store orchestration in the hot-band epilogue.
- dir_02: Retune PTX Prefetch Handoff In The K Loop | bottleneck: Copy-pipeline handoff timing inside the PTX hot-band steady-state loop.
- dir_03: Tune PTX Hot-Band B-Shared Skew Without Touching Traversal | bottleneck: Shared-memory layout and fragment address generation for PTX hot-band B loads.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
