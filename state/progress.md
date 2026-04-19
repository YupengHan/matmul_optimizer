# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `56038948d7d255701cbdaf6c5969d0fbc56b4aa7`
- plateau counter: `2`
- round loop: `round 8/20`
- rounds remaining: `13`
- notes: `Node A completed round 7/20. Run node_b to continue round 8/20.`

## Latest measured custom run

- run id: `20260418_232047_bf16_gemm_v1_5603894`
- run dir: `runs/20260418_232047_bf16_gemm_v1_5603894`
- correctness: `PASS`
- median runtime: `54.193089 ms`
- TFLOP/s: `13.415353 TFLOP/s`
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
