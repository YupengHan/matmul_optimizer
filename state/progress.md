# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f5de2e9ce546b72f0e2b1ecde0fbe5a766a31e42`
- plateau counter: `0`
- round loop: `round 4/20`
- rounds remaining: `17`
- notes: `Node C build succeeded for round 4/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_224421_bf16_gemm_v1_f5de2e9`
- run dir: `runs/20260418_224421_bf16_gemm_v1_f5de2e9`
- correctness: `PASS`
- median runtime: `65.617920 ms`
- TFLOP/s: `11.079587 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_224925`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- dir_01: Reuse one 16x16 epilogue scratch tile per warp with warp-synchronous pair stores | bottleneck: Shared-memory footprint and epilogue traffic are still constraining residency and keeping tensor utilization low after the B-tile skew fix. The current `c_shared` design stores all three output tiles per warp at once even though they are consumed strictly one tile at a time.
- dir_02: Prototype a shuffle-assisted BF16 pair-packing epilogue after each WMMA store | bottleneck: The current epilogue converts and stores each output element as a scalar BF16 write after a shared-memory round-trip, which may be amplifying short scoreboard and writeback pressure even after the main tensor loop improved.
- dir_03: Investigate a fragment-unpack path that bypasses `c_shared` entirely | bottleneck: The `c_shared` round-trip may be fundamentally unnecessary overhead once the tensor loop itself is healthy, but the current WMMA abstraction makes a direct path difficult.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `39.700031 ms`, `2.531762x` slower than CUTLASS
