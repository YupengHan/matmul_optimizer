# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3d01edf5053f250aa4096cda3efec53e1e8b894b`
- plateau counter: `0`
- round loop: `round 15/20`
- rounds remaining: `6`
- notes: `Node A completed round 14/20. Run node_b to continue round 15/20.`

## Latest measured custom run

- run id: `20260419_190546_bf16_gemm_v1_3d01edf`
- run dir: `runs/20260419_190546_bf16_gemm_v1_3d01edf`
- correctness: `PASS`
- median runtime: `30.062544 ms`
- TFLOP/s: `24.183563 TFLOP/s`
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
- current best custom gap: `4.144655 ms`, `1.159915x` slower than CUTLASS
