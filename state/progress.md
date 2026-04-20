# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9e7679d84de81ed2499e78ee6e3285f74206a441`
- plateau counter: `2`
- round loop: `round 3/50`
- rounds remaining: `48`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 3/50.`

## Latest measured custom run

- run id: `20260419_223856_bf16_gemm_v1_9e7679d`
- run dir: `runs/20260419_223856_bf16_gemm_v1_9e7679d`
- correctness: `PASS`
- median runtime: `30.578688 ms`
- TFLOP/s: `23.775364 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_223942`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/50 starts from another small bank-padding regression. The hot-band path remains dominant, and the recent local layout/export tweaks have not produced a durable win. Recommended direction dir_01 therefore moves to a larger but still coherent structural change: restore the current best surface and replace the final 64 hot rows with a dedicated 64x128 residual PTX kernel so those rows stop paying the 384 peeled path. Dir_02 is the restore fallback if that kernel does not validate quickly, and dir_03 defers any more export work until the residual path is specialized.`
- dir_01: Restore the best surface and replace the last 64 hot rows with a dedicated 64x128 residual PTX kernel | bottleneck: Residual hot-row overhead from routing the last 64 rows through the generic 384 peeled kernel instead of a matching fixed-shape PTX path.
- dir_02: Restore-only fallback to the current best surface | bottleneck: Not a bottleneck attack; this is the restore path after a negative bank-padding experiment.
- dir_03: Later: revisit export trimming only after the residual path is specialized | bottleneck: Shared epilogue/export overhead after the residual path has been unified with the PTX hot-band family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
