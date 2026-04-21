# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f07f87369857b40b150667abd9157c5a2408062f`
- plateau counter: `23`
- round loop: `round 36/100`
- rounds remaining: `65`
- notes: `Node C build succeeded for round 36/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_074828_bf16_gemm_v1_f07f873`
- run dir: `runs/20260421_074828_bf16_gemm_v1_f07f873`
- correctness: `PASS`
- median runtime: `24.175471 ms`
- TFLOP/s: `30.072606 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_075055`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 36 should not waste another slot on restore. The loop is already back on a clean PTX anchor, and the latest measurement at 24.175471 ms is close enough to the accepted 24.164272 ms baseline to resume real exploration. The ranking therefore moves back to live, unabsorbed families on the accepted surface: a bounded PTX control-path exploit first, the broader 256x128 low-register branch second, and a narrower steady-state handoff retime third.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and live-range pressure on the accepted one-K 128x128 branch.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.
- dir_03: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the active PTX hot-band steady-state loop, especially the handoff between MMA issue completion and future-tile refill.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
