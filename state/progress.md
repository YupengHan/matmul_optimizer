# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `06ebe93a00afa1ff8f20c5f4b4c89ec9cf1bbe89`
- plateau counter: `3`
- round loop: `round 62/100`
- rounds remaining: `39`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 62/100.`

## Latest measured custom run

- run id: `20260420_090210_bf16_gemm_v1_06ebe93`
- run dir: `runs/20260420_090210_bf16_gemm_v1_06ebe93`
- correctness: `PASS`
- median runtime: `25.634208 ms`
- TFLOP/s: `28.361299 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_090253`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_090210_bf16_gemm_v1_06ebe93 at 25.634208 ms. Rejected this round: grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, broad shared-memory rewrites, and consumer-order variants that replace the accepted right-left sweep as the active base.`
- dir_01: restore accepted base, then narrow locality window | bottleneck: Hot-band consumer-path locality and reuse window width on the accepted PTX sweep / handoff path.
- dir_02: accepted base, then narrow overlap recovery | bottleneck: Refill-order overlap around the one-sync handoff and staged consumer refill path.
- dir_03: final consumer-order closure | bottleneck: Residual consumer-order inefficiency in the hot-band PTX consumer path rather than grouping or refill layout.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
