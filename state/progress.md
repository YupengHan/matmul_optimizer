# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9062401adef4f69dbc37ff6dfca395d10895d20e`
- plateau counter: `65`
- round loop: `round 78/100`
- rounds remaining: `23`
- notes: `Node C is ready to implement auto_diagnosis_round_078:dir_01 via recommended selection for round 78/100.`

## Latest measured custom run

- run id: `20260421_084602_bf16_gemm_v1_9062401`
- run dir: `runs/20260421_084602_bf16_gemm_v1_9062401`
- correctness: `PASS`
- median runtime: `24.627200 ms`
- TFLOP/s: `29.520994 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_078`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 78 diagnosis. Recommended family: legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_03: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
