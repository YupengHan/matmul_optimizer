# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `19f846e10ffc1ed9f0dae8a6c25be01b4420802e`
- plateau counter: `8`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node A completed. Run node_b to produce exactly three directions from the latest measured summaries.`

## Latest measured custom run

- run id: `20260419_125734_bf16_gemm_v1_19f846e`
- run dir: `runs/20260419_125734_bf16_gemm_v1_19f846e`
- correctness: `PASS`
- median runtime: `36.371967 ms`
- TFLOP/s: `19.988455 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
