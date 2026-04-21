# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b026bf43674eb8b36dd321ef6673f8916a83105a`
- plateau counter: `31`
- round loop: `round 44/100`
- rounds remaining: `57`
- notes: `Node C is ready to implement auto_diagnosis_round_044:dir_01 via recommended selection for round 44/100.`

## Latest measured custom run

- run id: `20260421_083843_bf16_gemm_v1_b026bf4`
- run dir: `runs/20260421_083843_bf16_gemm_v1_b026bf4`
- correctness: `PASS`
- median runtime: `30.384064 ms`
- TFLOP/s: `23.927656 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_044`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 44 diagnosis. Recommended family: legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_02: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_03: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
