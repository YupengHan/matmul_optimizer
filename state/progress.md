# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b13027cdde2a90d1f00f3bd9b1e6b355ea15f2d9`
- plateau counter: `0`
- round loop: `round 16/20`
- rounds remaining: `5`
- notes: `Node A completed round 15/20. Run node_b to continue round 16/20.`

## Latest measured custom run

- run id: `20260419_191708_bf16_gemm_v1_b13027c`
- run dir: `runs/20260419_191708_bf16_gemm_v1_b13027c`
- correctness: `PASS`
- median runtime: `30.052768 ms`
- TFLOP/s: `24.191430 TFLOP/s`
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
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
