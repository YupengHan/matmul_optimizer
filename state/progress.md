# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8ba4496bd875ded3332c99af47abbc3b9c3d464b`
- plateau counter: `2`
- round loop: `round 6/20`
- rounds remaining: `15`
- notes: `Node C is ready to implement diagnosis_20260420_222929:dir_01 via recommended selection for round 6/20.`

## Latest measured custom run

- run id: `20260420_222846_bf16_gemm_v1_8ba4496`
- run dir: `runs/20260420_222846_bf16_gemm_v1_8ba4496`
- correctness: `PASS`
- median runtime: `24.535040 ms`
- TFLOP/s: `29.631883 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_222929`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/20 audit: the round-5 B-first prologue staging tweak measured 24.535040 ms, only 0.015872 ms slower than the previous run, but it moved the wrong counters: active warps slipped from 16.60% to 16.49%, barrier rose from 5.18% to 5.33%, and long-scoreboard rose from 7.28% to 7.50% while registers stayed pinned at the same occupancy ceiling. That is strong evidence that another copy-order micro-tune is not the best immediate use of budget. The diagnosis therefore promotes the rehydrated register-pressure family to rank 1, keeps a narrower PTX export cleanup as the active-branch fallback, and preserves one historical PTX grouping-window restore as the restore-style fallback family. This uses the live queue expansion from round_history instead of letting the loop collapse back to only one or two families.`
- dir_01: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register-limited occupancy and weak latency hiding caused by helper-induced live ranges in the PTX hot-band compute path.
- dir_02: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: PTX export-side address/control overhead and scratch management after MMA, rather than another feed-order or traversal issue.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Inter-CTA locality and launch-order mapping on the accepted PTX surface, but explicitly as a restore fallback rather than the primary next attack.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.740225 ms`, `0.932856x` slower than CUTLASS
