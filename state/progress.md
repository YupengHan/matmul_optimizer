# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `fe097e98f5e51da7e72c909a85c76f35a8c9508a`
- plateau counter: `2`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node A completed round 2/5. Run node_b to continue round 3/5.`

## Latest measured custom run

- run id: `20260419_094829_bf16_gemm_v1_fe097e9`
- run dir: `runs/20260419_094829_bf16_gemm_v1_fe097e9`
- correctness: `PASS`
- median runtime: `42.673632 ms`
- TFLOP/s: `17.036737 TFLOP/s`
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
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
