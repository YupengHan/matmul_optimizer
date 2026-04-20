# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9ee9b48dfb73b37b1d93ab38ac84f5dd17f596a2`
- plateau counter: `2`
- round loop: `round 61/100`
- rounds remaining: `40`
- notes: `Node C build succeeded for round 61/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_085928_bf16_gemm_v1_9ee9b48`
- run dir: `runs/20260420_085928_bf16_gemm_v1_9ee9b48`
- correctness: `PASS`
- median runtime: `25.821696 ms`
- TFLOP/s: `28.155370 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_090007`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to the latest measured run 20260420_085928_bf16_gemm_v1_9ee9b48 at 25.821696 ms. Keep the accepted grouped_rows=8 base, reversed PTX row-pair traversal, right-left PTX column sweep, and one-sync wait_group_0 handoff as the primary baseline; keep split sweep, full mirrored sweep, grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites closed for this round.`
- dir_01: Restore accepted base, then retime refill issue order | bottleneck: Refill issue ordering after the accepted one-sync handoff, not the consumer sweep order itself.
- dir_02: Minimal overlap recovery behind the one-sync handoff | bottleneck: Residual overlap loss in the steady-state handoff window after the accepted consumer path has already drained.
- dir_03: Very local consumer-order closure only | bottleneck: Residual consumer-side locality loss in the hot-band PTX sweep, limited to a small ordering closure.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
