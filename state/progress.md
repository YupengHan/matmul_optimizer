# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2668282cfb6bcf377df99fc25b0aefbbcdf90aec`
- plateau counter: `1`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260418_193855_bf16_gemm_v1_2668282`
- run dir: `runs/20260418_193855_bf16_gemm_v1_2668282`
- correctness: `PASS`
- median runtime: `813.605438 ms`
- TFLOP/s: `0.893577 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_194629`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Rewrite the steady-state tile around BF16 Tensor Cores | bottleneck: Tensor Core under-utilization
- dir_02: Keep tiles in BF16 and add a staged vectorized copy pipeline | bottleneck: Global-memory and shared-memory staging pressure
- dir_03: Split the fixed-shape steady state from edge cleanup | bottleneck: Tail-handling overhead from generic code and excess synchronization

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `776.924671 ms`, `30.976387x` slower than CUTLASS
