# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f8e7058c29b7f3cee19fb36701f9b82e048961e5`
- plateau counter: `2`
- round loop: `round 38/100`
- rounds remaining: `63`
- notes: `Node A completed round 37/100. Run node_b to continue round 38/100.`

## Latest measured custom run

- run id: `20260420_011851_bf16_gemm_v1_f8e7058`
- run dir: `runs/20260420_011851_bf16_gemm_v1_f8e7058`
- correctness: `PASS`
- median runtime: `26.150880 ms`
- TFLOP/s: `27.800955 TFLOP/s`
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
- current best custom gap: `0.175679 ms`, `1.006778x` slower than CUTLASS
