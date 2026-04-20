# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `761d868c89340f65e01ba99eb7c5c6492df9c893`
- plateau counter: `1`
- round loop: `round 58/100`
- rounds remaining: `43`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 58/100.`

## Latest measured custom run

- run id: `20260420_084554_bf16_gemm_v1_761d868`
- run dir: `runs/20260420_084554_bf16_gemm_v1_761d868`
- correctness: `PASS`
- median runtime: `25.473536 ms`
- TFLOP/s: `28.540184 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_084642`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to measured run 20260420_084554_bf16_gemm_v1_761d868 at 25.473536 ms. Round 56 accepted base at 24.713584 ms remains the target comparison; grouped_rows=16, warmup-order reopen, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, and broad shared-memory rewrites are rejected this round.`
- dir_01: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side PTX hot-band ordering and export latency in bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, especially around the grouped-row dispatch and the consumer/export handoff.
- dir_02: Recover overlap behind the accepted wait_group_0 handoff | bottleneck: Async refill overlap in the peeled PTX hot-band path, including the one-sync handoff in the PTX microkernel loop and the peeled hot-stage advance helper.
- dir_03: Smaller locality retune as a closure path | bottleneck: Residual launch-order locality and row-pair adjacency effects in the grouped hot-band consumer path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.204305 ms`, `0.953534x` slower than CUTLASS
