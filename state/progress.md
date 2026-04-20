# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `52a3af636bfe7050aaf0eeab255ff6c111eb0e01`
- plateau counter: `8`
- round loop: `round 7/20`
- rounds remaining: `14`
- notes: `Node A completed round 6/20. Run node_b to continue round 7/20.`

## Latest measured custom run

- run id: `20260419_174642_bf16_gemm_v1_52a3af6`
- run dir: `runs/20260419_174642_bf16_gemm_v1_52a3af6`
- correctness: `PASS`
- median runtime: `33.716736 ms`
- TFLOP/s: `21.562568 TFLOP/s`
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
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
