# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f84c2cd9587de8784372488625ecbb39332999c1`
- plateau counter: `58`
- round loop: `round 71/100`
- rounds remaining: `30`
- notes: `Node C is ready to implement auto_diagnosis_round_071:dir_01 via recommended selection for round 71/100.`

## Latest measured custom run

- run id: `20260421_084449_bf16_gemm_v1_f84c2cd`
- run dir: `runs/20260421_084449_bf16_gemm_v1_f84c2cd`
- correctness: `PASS`
- median runtime: `24.433151 ms`
- TFLOP/s: `29.755450 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_071`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 71 diagnosis. Recommended family: legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
