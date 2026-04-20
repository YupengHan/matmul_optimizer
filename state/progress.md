# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- plateau counter: `0`
- round loop: `round 1/50`
- rounds remaining: `50`
- notes: `Node C build succeeded for round 1/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_222734_bf16_gemm_v1_0d78758`
- run dir: `runs/20260419_222734_bf16_gemm_v1_0d78758`
- correctness: `PASS`
- median runtime: `29.325824 ms`
- TFLOP/s: `24.791100 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_223457`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/50 starts from the current best custom measurement at 29.325824 ms. The hot-band kernel still dominates and recent copy / consumer changes mostly regressed, so the next defensible move is to attack the export side. Recommended direction dir_01 keeps the same accumulator layout and shared footprint but changes the 64x64 export batching from horizontal pairs to vertical pairs, which should reduce warp-sync count in the hot-band epilogue. Dir_02 is a strict best-commit re-anchor fallback, and dir_03 records that fixed-shape peeling should only be revisited after the export behavior becomes simpler.`
- dir_01: Trim the hot-band export path by batching 64x64 stores vertically instead of horizontally | bottleneck: Hot-band epilogue / export synchronization and shared-memory round-trip overhead.
- dir_02: Re-anchor explicitly at the current best custom commit before more export work | bottleneck: Workflow / baseline drift rather than a micro-bottleneck.
- dir_03: Revisit stage peeling only after export behavior is simpler | bottleneck: Fixed-shape control and epilogue interaction after export simplification.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
