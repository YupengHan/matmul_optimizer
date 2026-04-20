# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0cbbcf7b2d28ba864853823c4120f8f0001843a1`
- plateau counter: `2`
- round loop: `round 24/50`
- rounds remaining: `27`
- notes: `Node A completed round 23/50. Run node_b to continue round 24/50.`

## Latest measured custom run

- run id: `20260420_001413_bf16_gemm_v1_0cbbcf7`
- run dir: `runs/20260420_001413_bf16_gemm_v1_0cbbcf7`
- correctness: `PASS`
- median runtime: `29.179888 ms`
- TFLOP/s: `24.915086 TFLOP/s`
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
- current best custom gap: `3.031615 ms`, `1.116970x` slower than CUTLASS
