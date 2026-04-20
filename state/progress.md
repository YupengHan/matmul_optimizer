# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `863f60f44803e7321464511c84f57f7dd24133e3`
- plateau counter: `5`
- round loop: `round 64/100`
- rounds remaining: `37`
- notes: `Node C build succeeded for round 64/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_091330_bf16_gemm_v1_863f60f`
- run dir: `runs/20260420_091330_bf16_gemm_v1_863f60f`
- correctness: `PASS`
- median runtime: `25.934336 ms`
- TFLOP/s: `28.033084 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_091413`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_091330_bf16_gemm_v1_863f60f at 25.934336 ms. Rejected this round: grouped_rows=16 active path, grouped_rows=4 active path, unroll 1 active path, warmup-order reopen, K32 cadence, extra-live B lookahead, CTA-level B repack, broad shared-memory rewrites, split sweep, and full mirrored sweep.`
- dir_01: Restore accepted grouped_rows=8 base, then test 8->6 hot-band narrowing | bottleneck: Locality loss in the hot-band PTX consumer ordering and row reuse window, not the broader sweep or sync structure.
- dir_02: Restore accepted base, then probe a very narrow overlap-recovery tweak | bottleneck: Residual consumer-to-producer overlap loss at the handoff boundary rather than the main sweep or row-group structure.
- dir_03: Restore accepted base, then revisit a very local consumer-order closure | bottleneck: A small ordering inefficiency in the consumer sequence inside the right-left sweep family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
