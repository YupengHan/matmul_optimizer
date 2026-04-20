# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `81bde72e538f33c457ea3cac1335513761c90fd6`
- plateau counter: `40`
- round loop: `round 15/17`
- rounds remaining: `3`
- notes: `Node A completed round 14/17. Run node_b to continue round 15/17.`

## Latest measured custom run

- run id: `20260420_163637_bf16_gemm_v1_81bde72`
- run dir: `runs/20260420_163637_bf16_gemm_v1_81bde72`
- correctness: `PASS`
- median runtime: `25.654704 ms`
- TFLOP/s: `28.338640 TFLOP/s`
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
