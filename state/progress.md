# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0cd407cfef0a9ca819c94d99ce74a28a295fced8`
- plateau counter: `3`
- round loop: `round 16/100`
- rounds remaining: `85`
- notes: `Node C is ready to implement diagnosis_20260421_001509:dir_01 via recommended selection for round 16/100.`

## Latest measured custom run

- run id: `20260421_001009_bf16_gemm_v1_0cd407c`
- run dir: `runs/20260421_001009_bf16_gemm_v1_0cd407c`
- correctness: `PASS`
- median runtime: `24.171008 ms`
- TFLOP/s: `30.078159 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_001509`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16 treats the latest PTX control-path result as a flat-positive continuation rather than a decisive closeout: the branch improved the accepted-base runtime slightly but not enough to replace the best-known 24.164272 ms run or to promote the accepted base in search state. The absorbed restore/export-cleanup families stay filtered out on the current source, while grouped_rows=8 and the 256x128 pivot branch remain explicitly live because the user asked to repopulate the frontier from promising round_history states after the search-policy update.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual cp.async handoff and inner-loop control overhead in the active 128x128 PTX hot-band microkernel, not DRAM bandwidth saturation and not another restore-only action.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the same steady-state wait/commit seam targeted by dir_01.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path, not the current 128x128 PTX wait/commit seam.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
