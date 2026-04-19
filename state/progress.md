# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `95056ed21eab5afe9e0a7fc2faefa6e3b29e3903`
- plateau counter: `0`
- round loop: `round 3/20`
- rounds remaining: `18`
- notes: `Node A completed round 2/20. Run node_b to continue round 3/20.`

## Latest measured custom run

- run id: `20260418_222639_bf16_gemm_v1_95056ed`
- run dir: `runs/20260418_222639_bf16_gemm_v1_95056ed`
- correctness: `PASS`
- median runtime: `66.354687 ms`
- TFLOP/s: `10.956565 TFLOP/s`
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
- current best custom gap: `40.436798 ms`, `2.560189x` slower than CUTLASS
