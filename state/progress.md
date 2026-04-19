# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `33e1461e09c0f90b0896452a94c16277f2a251db`
- plateau counter: `0`
- round loop: `round 18/20`
- rounds remaining: `3`
- notes: `Node A completed round 17/20. Run node_b to continue round 18/20.`

## Latest measured custom run

- run id: `20260419_011243_bf16_gemm_v1_33e1461`
- run dir: `runs/20260419_011243_bf16_gemm_v1_33e1461`
- correctness: `PASS`
- median runtime: `41.534977 ms`
- TFLOP/s: `17.503788 TFLOP/s`
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
- current best custom gap: `15.617088 ms`, `1.602560x` slower than CUTLASS
