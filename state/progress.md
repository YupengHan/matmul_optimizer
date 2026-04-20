# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a4646fcde92b3595f4801eb30c4e0026914da3a1`
- plateau counter: `2`
- round loop: `round 19/50`
- rounds remaining: `32`
- notes: `Node A completed round 18/50. Run node_b to continue round 19/50.`

## Latest measured custom run

- run id: `20260420_000122_bf16_gemm_v1_a4646fc`
- run dir: `runs/20260420_000122_bf16_gemm_v1_a4646fc`
- correctness: `PASS`
- median runtime: `31.673856 ms`
- TFLOP/s: `22.953297 TFLOP/s`
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
- current best custom gap: `3.287104 ms`, `1.126828x` slower than CUTLASS
