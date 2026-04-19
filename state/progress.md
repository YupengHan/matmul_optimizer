# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1e399d80f7b02720493e3275ecb2c6865cbe1e63`
- plateau counter: `0`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node A completed round 3/5. Run node_b to continue round 4/5.`

## Latest measured custom run

- run id: `20260419_135930_bf16_gemm_v1_1e399d8`
- run dir: `runs/20260419_135930_bf16_gemm_v1_1e399d8`
- correctness: `PASS`
- median runtime: `33.366047 ms`
- TFLOP/s: `21.789199 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

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
- current best custom gap: `7.448158 ms`, `1.287375x` slower than CUTLASS
