# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6ae3d5dde945d7280c330554c03cd23242093c26`
- plateau counter: `2`
- round loop: `round 7/30`
- rounds remaining: `24`
- notes: `Node C build succeeded for round 7/30. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_221542_bf16_gemm_v1_6ae3d5d`
- run dir: `runs/20260419_221542_bf16_gemm_v1_6ae3d5d`
- correctness: `PASS`
- median runtime: `30.304256 ms`
- TFLOP/s: `23.990670 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_221629`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/30 starts from the same implementation surface as the previously measured best custom, although the latest remeasurement landed closer to 30.30 ms than 29.43 ms. The code surface is therefore stable enough to continue experimentation without another restore-only round. Recommended direction dir_01 now follows the user-provided bank-conflict / register-reuse guidance directly: keep everything footprint-neutral and warp-local, but reverse the 64x64 B-consumer sweep into a `Right Left Right Left` order so the hot-band PTX path tests a different operand-delivery pattern. Dir_02 keeps the fixed-shape stage-peeling idea in reserve for the hot-band loop, and dir_03 captures the remaining coalescing / async-copy ownership experiment.`
- dir_01: Human idea bank conflict: reverse the mirrored 64x64 B sweep into a `Right Left Right Left` order | bottleneck: Residual warp-local B delivery / bank behavior inside the 64x64 hot-band consumer path.
- dir_02: Human idea stage: peel the hot-band K loop into fixed-shape prologue / steady-state / epilogue | bottleneck: Fixed-shape control-flow and stage-transition overhead inside the hot-band pipeline.
- dir_03: Human idea coalescing + async copy: retune hot-band cp.async ownership into contiguous warp stripes | bottleneck: Global-to-shared staging issue regularity and instruction ownership rather than raw bandwidth.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
