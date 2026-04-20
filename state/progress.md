# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6ae3d5dde945d7280c330554c03cd23242093c26`
- plateau counter: `2`
- round loop: `round 7/30`
- rounds remaining: `24`
- notes: `Node A completed round 6/30. Run node_b to continue round 7/30.`

## Latest measured custom run

- run id: `20260419_221542_bf16_gemm_v1_6ae3d5d`
- run dir: `runs/20260419_221542_bf16_gemm_v1_6ae3d5d`
- correctness: `PASS`
- median runtime: `30.304256 ms`
- TFLOP/s: `23.990670 TFLOP/s`
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
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
