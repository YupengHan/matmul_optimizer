# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- plateau counter: `0`
- round loop: `round 11/30`
- rounds remaining: `20`
- notes: `Node A completed round 10/30. Run node_b to continue round 11/30.`

## Latest measured custom run

- run id: `20260419_222734_bf16_gemm_v1_0d78758`
- run dir: `runs/20260419_222734_bf16_gemm_v1_0d78758`
- correctness: `PASS`
- median runtime: `29.325824 ms`
- TFLOP/s: `24.791100 TFLOP/s`
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
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
