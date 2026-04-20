# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `848bad76a95cfcc18a02981190b09432583d4aa5`
- plateau counter: `1`
- round loop: `round 2/50`
- rounds remaining: `49`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 2/50.`

## Latest measured custom run

- run id: `20260419_223649_bf16_gemm_v1_848bad7`
- run dir: `runs/20260419_223649_bf16_gemm_v1_848bad7`
- correctness: `PASS`
- median runtime: `30.356480 ms`
- TFLOP/s: `23.949398 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_223724`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/50 starts from a neutral export rewrite. The hot-band kernel remained essentially unchanged at about 41.10 ms while end-to-end runtime regressed, so the best next move is not more export work. Recommended direction dir_01 returns to the user-provided bank-conflict family with the smallest viable layout change: increase the hot-band B shared-memory skew from +8 elements to +16 elements while leaving tile shape, stage depth, and consumer order untouched. Dir_02 is the restore fallback if that padding is neutral or negative, and dir_03 explicitly defers more export work until the bank-layout side has been re-tested.`
- dir_01: Human idea bank conflict: increase the hot-band B shared-memory padding from +8 to +16 elements | bottleneck: Residual B-side shared-memory bank behavior in the hot-band WMMA/PTX consumer path.
- dir_02: Restore-only fallback if the larger B padding regresses | bottleneck: Not a direct bottleneck attack; this is the restore path after a footprint-only experiment.
- dir_03: Later: revisit export path only if bank padding gives a measurable signal | bottleneck: Secondary export-side overhead after the operand-delivery path is re-tuned.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
