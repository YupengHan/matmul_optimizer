# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `95723fb3a7d1c934573fd5a2c38d3705e46bd2c2`
- plateau counter: `4`
- round loop: `round 17/100`
- rounds remaining: `84`
- notes: `Node C is ready to implement diagnosis_20260421_002435:dir_01 via recommended selection for round 17/100.`

## Latest measured custom run

- run id: `20260421_002405_bf16_gemm_v1_95723fb`
- run dir: `runs/20260421_002405_bf16_gemm_v1_95723fb`
- correctness: `PASS`
- median runtime: `24.190864 ms`
- TFLOP/s: `30.053471 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_002435`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17 explicitly treats the latest PTX wait-window retime as negative evidence. The current source no longer matches the best measured PTX surface: it differs by the round-15 future_tile_k hoist and the round-16 prologue wait retime, and the latter pushed runtime back up to 24.190864 ms. The immediate recommendation is therefore a direct PTX-surface restore, while grouped_rows=8 and the 256x128 pivot branch remain live because the user asked to repopulate promising round_history families into the active search queue.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the proven PTX winner surface, specifically the prologue wait window and refill-address hot-band seam, not a need for another fresh PTX control experiment on top of the regressed variant.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer locality in the PTX hot-band microkernel, not the same prologue wait seam that just regressed.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path rather than another narrow PTX wait/commit change.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
