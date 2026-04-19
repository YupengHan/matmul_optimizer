# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `91e446eea2cf2de912e81e21c45653dcd227d591`
- plateau counter: `0`
- round loop: `round 6/20`
- rounds remaining: `15`
- notes: `Node A completed round 5/20. Run node_b to continue round 6/20.`

## Latest measured custom run

- run id: `20260418_225901_bf16_gemm_v1_91e446e`
- run dir: `runs/20260418_225901_bf16_gemm_v1_91e446e`
- correctness: `PASS`
- median runtime: `54.136911 ms`
- TFLOP/s: `13.429274 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

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
