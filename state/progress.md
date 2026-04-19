# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6bee469ece2906ab9efdd498b44f9b8d05b6e1bc`
- plateau counter: `3`
- round loop: `round 9/20`
- rounds remaining: `12`
- notes: `Node A completed round 8/20. Run node_b to continue round 9/20.`

## Latest measured custom run

- run id: `20260418_233053_bf16_gemm_v1_6bee469`
- run dir: `runs/20260418_233053_bf16_gemm_v1_6bee469`
- correctness: `PASS`
- median runtime: `56.870047 ms`
- TFLOP/s: `12.783872 TFLOP/s`
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
