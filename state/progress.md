# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `00919407eb22d3b9a6679a2d22c9f6c64eb9680e`
- plateau counter: `77`
- round loop: `round 90/100`
- rounds remaining: `11`
- notes: `Node C is ready to implement auto_diagnosis_round_090:dir_01 via recommended selection for round 90/100.`

## Latest measured custom run

- run id: `20260421_084801_bf16_gemm_v1_0091940`
- run dir: `runs/20260421_084801_bf16_gemm_v1_0091940`
- correctness: `PASS`
- median runtime: `24.747520 ms`
- TFLOP/s: `29.377465 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_090`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 90 diagnosis. Recommended family: legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
