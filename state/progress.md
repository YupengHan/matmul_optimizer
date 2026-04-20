# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1b9dbe3d306090b4f1762f1e1a504c13d2ab5d92`
- plateau counter: `0`
- round loop: `round 32/50`
- rounds remaining: `19`
- notes: `Node A completed round 31/50. Run node_b to continue round 32/50.`

## Latest measured custom run

- run id: `20260420_002759_bf16_gemm_v1_1b9dbe3`
- run dir: `runs/20260420_002759_bf16_gemm_v1_1b9dbe3`
- correctness: `PASS`
- median runtime: `26.924031 ms`
- TFLOP/s: `27.002621 TFLOP/s`
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
- current best custom gap: `1.006143 ms`, `1.038820x` slower than CUTLASS
