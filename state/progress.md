# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `61be2e8be6b96d4f3c3424f3e8f2b3b307b7293e`
- plateau counter: `11`
- round loop: `round 6/10`
- rounds remaining: `5`
- notes: `Node A completed round 5/10. Run node_b to continue round 6/10.`

## Latest measured custom run

- run id: `20260419_210551_bf16_gemm_v1_61be2e8`
- run dir: `runs/20260419_210551_bf16_gemm_v1_61be2e8`
- correctness: `PASS`
- median runtime: `30.570496 ms`
- TFLOP/s: `23.781735 TFLOP/s`
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
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
