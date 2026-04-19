# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a4966f51626c0ae4e2d99e4e49fe26264639b123`
- plateau counter: `0`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node C build succeeded. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_195405_bf16_gemm_v1_a4966f5`
- run dir: `runs/20260418_195405_bf16_gemm_v1_a4966f5`
- correctness: `PASS`
- median runtime: `298.095123 ms`
- TFLOP/s: `2.438884 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_200741`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- dir_01: Add CTA-level shared-memory staging for WMMA tiles | bottleneck: Global-memory bound
- dir_02: Retune the WMMA tile hierarchy for more per-warp accumulation | bottleneck: Tensor Core under-utilization
- dir_03: Specialize the hot path to the fixed aligned benchmark shape | bottleneck: Tail-handling overhead from generic code

## Active implementation direction

- direction id: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `272.177235 ms`, `11.501520x` slower than CUTLASS
