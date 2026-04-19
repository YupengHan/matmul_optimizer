# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c2f2bec47c9cba44f35cf7d260893f0416a4d251`
- plateau counter: `0`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node A completed round 2/5. Run node_b to continue round 3/5.`

## Latest measured custom run

- run id: `20260419_132725_bf16_gemm_v1_c2f2bec`
- run dir: `runs/20260419_132725_bf16_gemm_v1_c2f2bec`
- correctness: `PASS`
- median runtime: `34.234447 ms`
- TFLOP/s: `21.236488 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

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
- current best custom gap: `8.316559 ms`, `1.320881x` slower than CUTLASS
