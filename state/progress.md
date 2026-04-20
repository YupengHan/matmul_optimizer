# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3a888bc54495c13c7d85cfd5f98d2b64376e537f`
- plateau counter: `11`
- round loop: `round 70/100`
- rounds remaining: `31`
- notes: `Node A completed round 69/100. Run node_b to continue round 70/100.`

## Latest measured custom run

- run id: `20260420_105019_bf16_gemm_v1_3a888bc`
- run dir: `runs/20260420_105019_bf16_gemm_v1_3a888bc`
- correctness: `PASS`
- median runtime: `25.499136 ms`
- TFLOP/s: `28.511532 TFLOP/s`
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
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
