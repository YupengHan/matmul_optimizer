# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `79cdb4341e0f3a30327d811f49424bb324cbbf43`
- plateau counter: `0`
- round loop: `round 17/20`
- rounds remaining: `4`
- notes: `Node A completed round 16/20. Run node_b to continue round 17/20.`

## Latest measured custom run

- run id: `20260419_010405_bf16_gemm_v1_79cdb43`
- run dir: `runs/20260419_010405_bf16_gemm_v1_79cdb43`
- correctness: `PASS`
- median runtime: `42.564560 ms`
- TFLOP/s: `17.080393 TFLOP/s`
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
- current best custom gap: `16.646671 ms`, `1.642285x` slower than CUTLASS
