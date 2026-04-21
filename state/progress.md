# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `82c8e608fba26a9b0398984dd20ce199bb1d46f6`
- plateau counter: `3`
- round loop: `round 7/100`
- rounds remaining: `94`
- notes: `Node C is ready to implement diagnosis_20260420_223553:dir_01 via recommended selection for round 7/100.`

## Latest measured custom run

- run id: `20260420_223530_bf16_gemm_v1_82c8e60`
- run dir: `runs/20260420_223530_bf16_gemm_v1_82c8e60`
- correctness: `PASS`
- median runtime: `24.180656 ms`
- TFLOP/s: `30.066157 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_223553`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/100 audit: restoring the historical PTX grouping window and accepted-surface prologue delivered a real win, dropping runtime from 24.535040 ms to 24.180656 ms. That says the search should bank the restored surface and spend the next budget unit on a new family rather than immediately iterate the same restore knob again. The restored run still shows the familiar signature: 16.62% active warps, register-limited occupancy, barrier 5.48%, and long-scoreboard 7.17% with low DRAM pressure. That makes the PTX export-address/control surface the best next bounded family, with a second PTX control-path exploit and one off-branch export-scratch family kept alive behind it.`
- dir_01: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: PTX export-side address/control overhead and scratch bookkeeping on the restored accepted hot-band surface.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead on the restored grouping surface, not another locality or macro-tiling miss.
- dir_03: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: Export scratch lifetime and writeback overhead on the grouped-row 128x128 sibling path, used as an off-branch fallback family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.740225 ms`, `0.932856x` slower than CUTLASS
