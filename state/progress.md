# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b5784f4e9e43ef648fcb9c7fd9f71133b02c6fe3`
- plateau counter: `71`
- round loop: `round 84/100`
- rounds remaining: `17`
- notes: `Node C build succeeded for round 84/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_084701_bf16_gemm_v1_b5784f4`
- run dir: `runs/20260421_084701_bf16_gemm_v1_b5784f4`
- correctness: `PASS`
- median runtime: `30.694863 ms`
- TFLOP/s: `23.685377 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_084`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 84 diagnosis. Recommended family: legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_02: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_03: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
