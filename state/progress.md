# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `cb070a739eb38f4ea8ca9c5e0243a825338dbf67`
- plateau counter: `6`
- round loop: `round 15/50`
- rounds remaining: `36`
- notes: `Node A completed round 14/50. Run node_b to continue round 15/50.`

## Latest measured custom run

- run id: `20260420_194440_bf16_gemm_v1_cb070a7`
- run dir: `runs/20260420_194440_bf16_gemm_v1_cb070a7`
- correctness: `PASS`
- median runtime: `31.797344 ms`
- TFLOP/s: `22.864155 TFLOP/s`
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
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
