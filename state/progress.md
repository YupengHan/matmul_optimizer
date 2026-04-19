# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9bdc160ee2a6ef0f1171c09f4cf72f7dd081cab1`
- plateau counter: `2`
- round loop: `single-run`
- rounds remaining: `20`
- notes: `Node A completed. Run node_b to produce exactly three directions from the latest measured summaries.`

## Latest measured custom run

- run id: `20260419_142213_bf16_gemm_v1_9bdc160`
- run dir: `runs/20260419_142213_bf16_gemm_v1_9bdc160`
- correctness: `PASS`
- median runtime: `33.128447 ms`
- TFLOP/s: `21.945473 TFLOP/s`
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
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
