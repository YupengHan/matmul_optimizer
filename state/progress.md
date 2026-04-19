# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `134df2982fe154e85e9b0d1b62207275ee201a27`
- plateau counter: `2`
- round loop: `round 13/20`
- rounds remaining: `8`
- notes: `Node A completed round 12/20. Run node_b to continue round 13/20.`

## Latest measured custom run

- run id: `20260419_002116_bf16_gemm_v1_134df29`
- run dir: `runs/20260419_002116_bf16_gemm_v1_134df29`
- correctness: `PASS`
- median runtime: `46.005760 ms`
- TFLOP/s: `15.802791 TFLOP/s`
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
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
