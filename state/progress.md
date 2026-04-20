# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3dd4394d5113e6c6f6f2cc1e37c32dad490af6c4`
- plateau counter: `11`
- round loop: `round 10/20`
- rounds remaining: `11`
- notes: `Node A completed round 9/20. Run node_b to continue round 10/20.`

## Latest measured custom run

- run id: `20260419_181807_bf16_gemm_v1_3dd4394`
- run dir: `runs/20260419_181807_bf16_gemm_v1_3dd4394`
- correctness: `PASS`
- median runtime: `488.546341 ms`
- TFLOP/s: `1.488128 TFLOP/s`
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
