# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7864f5515778a7b40f754bd5cb6ac6e0ec083ef2`
- plateau counter: `2`
- round loop: `round 30/50`
- rounds remaining: `21`
- notes: `Node A completed round 29/50. Run node_b to continue round 30/50.`

## Latest measured custom run

- run id: `20260420_002455_bf16_gemm_v1_7864f55`
- run dir: `runs/20260420_002455_bf16_gemm_v1_7864f55`
- correctness: `PASS`
- median runtime: `30.668673 ms`
- TFLOP/s: `23.705604 TFLOP/s`
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
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
