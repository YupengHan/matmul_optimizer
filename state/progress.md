# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7adfc4eaef68ec1c5b773b611c0d7a91b594c7b8`
- plateau counter: `28`
- round loop: `round 3/17`
- rounds remaining: `15`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 3/17.`

## Latest measured custom run

- run id: `20260420_154827_bf16_gemm_v1_7adfc4e`
- run dir: `runs/20260420_154827_bf16_gemm_v1_7adfc4e`
- correctness: `PASS`
- median runtime: `25.505328 ms`
- TFLOP/s: `28.504610 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_154908`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/17 diagnosis for run 20260420_154827_bf16_gemm_v1_7adfc4e. Human-review mapping: continue to accept only narrow PTX-adjacent ideas on the recovered baseline; keep broad default-promotion, staged K32, paired export-lifetime, helper-flattening-without-locality-awareness, and x-major traversal closed. The key update is that the export-helper family is now confirmed live: the bounded row-pair specialization improved runtime to 25.50532818 ms while holding DRAM at 11.54 and reducing long-scoreboard to 7.21. That makes a final TileRow flattening pass the best next move, with PTX prefetch retiming and B-shared skew as the two backup families.`
- dir_01: Finish Flattening PTX Export Across Tile Rows | bottleneck: Residual PTX export-side control overhead and per-row epilogue orchestration inside the hot-band microkernel.
- dir_02: Retune PTX Prefetch Handoff After The Export Cleanup | bottleneck: Copy-pipeline handoff timing in the PTX hot-band steady-state loop.
- dir_03: Tune PTX Hot-Band B-Shared Skew On Top Of The New Base | bottleneck: Shared-memory fragment address generation and B-tile layout friction in the PTX hot-band path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
