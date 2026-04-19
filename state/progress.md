# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f5de2e9ce546b72f0e2b1ecde0fbe5a766a31e42`
- plateau counter: `0`
- round loop: `round 4/20`
- rounds remaining: `17`
- notes: `Node A completed round 3/20. Run node_b to continue round 4/20.`

## Latest measured custom run

- run id: `20260418_224421_bf16_gemm_v1_f5de2e9`
- run dir: `runs/20260418_224421_bf16_gemm_v1_f5de2e9`
- correctness: `PASS`
- median runtime: `65.617920 ms`
- TFLOP/s: `11.079587 TFLOP/s`
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
- current best custom gap: `39.700031 ms`, `2.531762x` slower than CUTLASS
