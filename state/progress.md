# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5ae2249d5b7a8c9f9686021e82e20d1a24aa3bde`
- plateau counter: `0`
- round loop: `round 25/50`
- rounds remaining: `26`
- notes: `Node A completed round 24/50. Run node_b to continue round 25/50.`

## Latest measured custom run

- run id: `20260420_001545_bf16_gemm_v1_5ae2249`
- run dir: `runs/20260420_001545_bf16_gemm_v1_5ae2249`
- correctness: `PASS`
- median runtime: `27.691520 ms`
- TFLOP/s: `26.254226 TFLOP/s`
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
- current best custom gap: `1.773631 ms`, `1.068433x` slower than CUTLASS
