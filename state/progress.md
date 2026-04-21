# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7febf056e40c5c640fbec693394bf6a7ed7727b7`
- plateau counter: `40`
- round loop: `round 53/100`
- rounds remaining: `48`
- notes: `Node C is ready to implement auto_diagnosis_round_053:dir_01 via recommended selection for round 53/100.`

## Latest measured custom run

- run id: `20260421_084009_bf16_gemm_v1_7febf05`
- run dir: `runs/20260421_084009_bf16_gemm_v1_7febf05`
- correctness: `PASS`
- median runtime: `24.426497 ms`
- TFLOP/s: `29.763557 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_053`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 53 diagnosis. Recommended family: legacy::port_grouped_row_traversal_into_the_non_ptx_128x128_sibling.`
- dir_01: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
