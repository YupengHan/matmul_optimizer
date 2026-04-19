# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `aee3c09b51fbf78ad79f4ce5f68841449bab54a1`
- plateau counter: `0`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 2/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_210900_bf16_gemm_v1_aee3c09`
- run dir: `runs/20260418_210900_bf16_gemm_v1_aee3c09`
- correctness: `PASS`
- median runtime: `101.374962 ms`
- TFLOP/s: `7.171588 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_210931`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Reduce cp.async barrier pressure | bottleneck: Barrier and wait-group serialization in the double-buffered steady-state loop.
- dir_02: Widen and repack the staging path | bottleneck: MIO throttle from cp.async issue rate and shared-memory staging layout.
- dir_03: Retune the tensor block geometry | bottleneck: Occupancy / register pressure limiting tensor-core issue efficiency.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `75.457073 ms`, `3.911390x` slower than CUTLASS
