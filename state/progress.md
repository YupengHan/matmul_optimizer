# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8138da55448e546af314940addc89fd3cadc56ff`
- plateau counter: `0`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node A completed round 3/5. Run node_b to continue round 4/5.`

## Latest measured custom run

- run id: `20260418_212627_bf16_gemm_v1_8138da5`
- run dir: `runs/20260418_212627_bf16_gemm_v1_8138da5`
- correctness: `PASS`
- median runtime: `97.885185 ms`
- TFLOP/s: `7.427267 TFLOP/s`
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
- current best custom gap: `71.967297 ms`, `3.776742x` slower than CUTLASS
