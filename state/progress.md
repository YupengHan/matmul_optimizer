# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b4f4a28d3f4f13c71f287127a37f5fe71a5b930c`
- plateau counter: `1`
- round loop: `round 27/50`
- rounds remaining: `24`
- notes: `Node A completed round 26/50. Run node_b to continue round 27/50.`

## Latest measured custom run

- run id: `20260420_001930_bf16_gemm_v1_b4f4a28`
- run dir: `runs/20260420_001930_bf16_gemm_v1_b4f4a28`
- correctness: `PASS`
- median runtime: `31.002625 ms`
- TFLOP/s: `23.450254 TFLOP/s`
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
- current best custom gap: `1.309376 ms`, `1.050520x` slower than CUTLASS
