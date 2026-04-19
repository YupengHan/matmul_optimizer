# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `95056ed21eab5afe9e0a7fc2faefa6e3b29e3903`
- plateau counter: `0`
- round loop: `round 3/20`
- rounds remaining: `18`
- notes: `Node C build succeeded for round 3/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_222639_bf16_gemm_v1_95056ed`
- run dir: `runs/20260418_222639_bf16_gemm_v1_95056ed`
- correctness: `PASS`
- median runtime: `66.354687 ms`
- TFLOP/s: `10.956565 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_222704`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- dir_01: Skew the B shared tile with a bank-conflict-avoidance swizzle | bottleneck: Residual bank conflicts and port contention on the shared-memory-to-WMMA B-fragment feed path, which still show up as `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 25.61` and `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct = 11.28` even after the tile-retune improvement.
- dir_02: Split the B tile into three independently padded 16x16 shared subtiles | bottleneck: The combined 16x48 row-major B layout may be making the three adjacent fragment loads interfere with each other at shared-memory bank granularity even though the per-warp compute reuse is otherwise correct.
- dir_03: Transpose B into a conflict-friendlier shared layout and switch the WMMA load orientation | bottleneck: The row-major B shared layout may be fundamentally mismatched to the warp-level matrix_b load pattern, keeping the tensor pipe underfed even after the earlier global-to-shared improvements.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `40.436798 ms`, `2.560189x` slower than CUTLASS
