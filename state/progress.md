# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c2190a99f9933c10afbc772d325b1873689314a6`
- plateau counter: `28`
- round loop: `round 41/100`
- rounds remaining: `60`
- notes: `Node C build succeeded for round 41/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_082405_bf16_gemm_v1_c2190a9`
- run dir: `runs/20260421_082405_bf16_gemm_v1_c2190a9`
- correctness: `PASS`
- median runtime: `24.180737 ms`
- TFLOP/s: `30.066058 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_041`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 41 diagnosis. Recommended family: legacy::restore_accepted_grouped_rows_8_hot_band_consumer_ordering.`
- dir_01: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
