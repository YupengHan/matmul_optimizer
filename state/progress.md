# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `57d08c3396876293a5e7c223a96cb3da09cca4a9`
- plateau counter: `0`
- round loop: `round 57/100`
- rounds remaining: `44`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 57/100.`

## Latest measured custom run

- run id: `20260420_084312_bf16_gemm_v1_57d08c3`
- run dir: `runs/20260420_084312_bf16_gemm_v1_57d08c3`
- correctness: `PASS`
- median runtime: `24.713584 ms`
- TFLOP/s: `29.417806 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_084408`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to measured run 20260420_084312_bf16_gemm_v1_57d08c3 at 24.713584 ms. Rejected this round: reopening warmup-order, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites.`
- dir_01: Hot-band L2 / grouped-row launch-order refinement | bottleneck: Improved L2 locality and reduced B-tile churn should trim long scoreboard pressure without reopening the already-accepted one-sync handoff base.
- dir_02: PTX hot-band consumer-order refinement | bottleneck: The warp consumer order inside the active PTX hot-band microkernel likely still leaves a small scoreboard gap after the retime.
- dir_03: Deferred steady-state overlap recovery | bottleneck: Residual handoff overlap and refill timing in the steady-state peeled hot-band path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.204305 ms`, `0.953534x` slower than CUTLASS
