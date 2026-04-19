# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2668282cfb6bcf377df99fc25b0aefbbcdf90aec`
- plateau counter: `1`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node C build succeeded. Node A will now measure the new code path.`

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
- approved direction: `dir_01`
- dir_01: Rewrite the steady-state tile around BF16 Tensor Cores | bottleneck: Tensor Core under-utilization
- dir_02: Keep tiles in BF16 and add a staged vectorized copy pipeline | bottleneck: Global-memory and shared-memory staging pressure
- dir_03: Split the fixed-shape steady state from edge cleanup | bottleneck: Tail-handling overhead from generic code and excess synchronization

## Active implementation direction

- direction id: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `776.924671 ms`, `30.976387x` slower than CUTLASS
