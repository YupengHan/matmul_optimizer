# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `634ee7b5da2e86c379ce3c7e90da488951c4e97a`
- plateau counter: `60`
- round loop: `round 73/100`
- rounds remaining: `28`
- notes: `Node C is ready to implement auto_diagnosis_round_073:dir_01 via recommended selection for round 73/100.`

## Latest measured custom run

- run id: `20260421_084511_bf16_gemm_v1_634ee7b`
- run dir: `runs/20260421_084511_bf16_gemm_v1_634ee7b`
- correctness: `PASS`
- median runtime: `24.420304 ms`
- TFLOP/s: `29.771104 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_073`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 73 diagnosis. Recommended family: legacy::restore_accepted_grouped_rows_8_hot_band_consumer_ordering.`
- dir_01: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
