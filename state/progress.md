# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1dd4420e7958cd21478c561c7169064f8b6f054b`
- plateau counter: `4`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 2/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_123228_bf16_gemm_v1_1dd4420`
- run dir: `runs/20260419_123228_bf16_gemm_v1_1dd4420`
- correctness: `PASS`
- median runtime: `42.259968 ms`
- TFLOP/s: `17.203502 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_123318`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Diagnosed regressed round-1 run 20260419_123228_bf16_gemm_v1_1dd4420 while ranking follow-ups against the restored accepted base 15d63b2. The warp-specialized producer/consumer split is strong negative evidence: it pushed the hot kernel to 219 registers per thread, dropped occupancy_limit_registers to 1, cut active warps to 16.60, and regressed to 42.259968 ms. The recommended follow-up therefore keeps the accepted 64x384 macro shape and targets lower-risk fixed-shape control overhead by splitting the hot path into explicit prologue, steady-state, and epilogue phases.`
- dir_01: Split the fixed 64x384 hot path into explicit prologue, steady-state, and epilogue phases | bottleneck: Fixed-shape hot-loop control and stage-transition overhead in the restored 64x384 peeled kernel, where tensor activity is still only 34.86 despite stable 2-block occupancy.
- dir_02: Straight-line the Tile384 cp.async producer schedule without warp specialization | bottleneck: Producer-side cp.async issue overhead and LSU address work in the hot kernel, without changing warp roles or macro-tile shape.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop, barrier, and scoreboard overhead in the 64x96 tail kernel; total upside is capped by the tail's small share of wall time.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
