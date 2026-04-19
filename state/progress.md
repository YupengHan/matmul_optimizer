# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `aee3c09b51fbf78ad79f4ce5f68841449bab54a1`
- plateau counter: `0`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node A completed round 1/5. Run node_b to continue round 2/5.`

## Latest measured custom run

- run id: `20260418_210900_bf16_gemm_v1_aee3c09`
- run dir: `runs/20260418_210900_bf16_gemm_v1_aee3c09`
- correctness: `PASS`
- median runtime: `101.374962 ms`
- TFLOP/s: `7.171588 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `75.457073 ms`, `3.911390x` slower than CUTLASS
