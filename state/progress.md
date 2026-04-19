# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2a86c71387e520f89bd133d824161d17428f4242`
- plateau counter: `1`
- round loop: `round 7/20`
- rounds remaining: `14`
- notes: `Node A completed round 6/20. Run node_b to continue round 7/20.`

## Latest measured custom run

- run id: `20260418_230727_bf16_gemm_v1_2a86c71`
- run dir: `runs/20260418_230727_bf16_gemm_v1_2a86c71`
- correctness: `PASS`
- median runtime: `57.120176 ms`
- TFLOP/s: `12.727892 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

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
- current best custom gap: `28.219023 ms`, `2.088786x` slower than CUTLASS
