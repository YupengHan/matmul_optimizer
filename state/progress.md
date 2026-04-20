# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4e5579ec72e9b1f05820c895c0315235d66f30cd`
- plateau counter: `0`
- round loop: `round 59/100`
- rounds remaining: `42`
- notes: `Node C build succeeded for round 59/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_084915_bf16_gemm_v1_4e5579e`
- run dir: `runs/20260420_084915_bf16_gemm_v1_4e5579e`
- correctness: `PASS`
- median runtime: `24.570881 ms`
- TFLOP/s: `29.588659 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_085345`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_084915_bf16_gemm_v1_4e5579e at 24.570881 ms. Accepted themes this round were Register Reuse, Ps2r, and Bank Conflict. Rejected this round: grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites.`
- dir_01: PTX hot-band consumer-order refinement | bottleneck: Long scoreboard latency in the PTX hot-band consumer path, not the barrier or shared-memory handoff itself.
- dir_02: Recover overlap behind the one-sync wait_group_0 handoff | bottleneck: Residual overlap loss after the single wait_group_0 + __syncthreads() handoff, now exposed mainly as long scoreboard.
- dir_03: Limited locality closure with grouped_rows=8 only | bottleneck: Minor locality loss in the grouped_rows=8 dispatch order, not a structural tile-size problem.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
