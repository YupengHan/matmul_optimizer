# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1653a82878dfc5f563cd0ff65442d526874aa9a3`
- plateau counter: `1`
- round loop: `round 54/100`
- rounds remaining: `47`
- notes: `Node C build succeeded for round 54/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_082654_bf16_gemm_v1_1653a82`
- run dir: `runs/20260420_082654_bf16_gemm_v1_1653a82`
- correctness: `PASS`
- median runtime: `24.904640 ms`
- TFLOP/s: `29.192127 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_082833`
- recommended direction: `dir_01`
- approved direction: `N/A`
- diagnosis notes: `Accepted this round: the B-first cp.async handoff family, constrained to the already-accepted grouped-row=8 + K16 + no-lookahead + single-scratch export base. Deferred: export/live-range trimming, because it is still plausible but secondary to the handoff retiming. Rejected: reopening the A-first warmup / B-first refill branch, because the latest experiment regressed and the evidence still points to steady-state handoff timing rather than warmup order.`
- dir_01: Retune the accepted B-first cp.async handoff inside the K16 hot band | bottleneck: Async-copy feed/issue retiming and stage handoff latency inside the active PTX hot-band microkernel.
- dir_02: Trim PTX export and accumulator live range on the accepted single-scratch surface | bottleneck: Register pressure and export-side synchronization / live-range overhead in the PTX hot-band epilogue.
- dir_03: Reopen the warmup A-first / refill B-first branch only as a closure probe | bottleneck: Warmup ordering is not the primary limiter; the current loss is in steady-state handoff timing on the accepted base.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.022401 ms`, `0.960552x` slower than CUTLASS
