# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `19f846e10ffc1ed9f0dae8a6c25be01b4420802e`
- plateau counter: `8`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_125734_bf16_gemm_v1_19f846e`
- run dir: `runs/20260419_125734_bf16_gemm_v1_19f846e`
- correctness: `PASS`
- median runtime: `36.371967 ms`
- TFLOP/s: `19.988455 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_125849`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Ranking is against the restored 19f846e baseline at 36.371967 ms. Round 1 warp specialization, round 3 producer straight-lining, and round 4 consumer-side B swizzle remain strong negative evidence and rule out further B-feed or occupancy-collapsing follow-ons. The round-18 autotune sweep still anchors 64x384 as the correct macro tile, so dir_01 is framed explicitly as epilogue budget for overlap: reduce c_shared/export cost only insofar as the saved bytes can buy more useful A/B overlap on the hot peeled kernel.`
- dir_01: Tile384 epilogue budget for overlap | bottleneck: The limiting factor is overlap budget inside the 64x384 peeled kernel: shared-memory allocation and epilogue round-trip pressure leave the hot loop underfed, which shows up as persistent mio throttle and only middling tensor activity despite low DRAM pressure.
- dir_02: Retimed two-stage recycle in the peeled hot loop | bottleneck: Barrier and issue-slot dilution inside the fixed peeled steady-state loop, not global memory bandwidth and not the macro tile width.
- dir_03: Fixed-shape peel and export cleanup for the 64x96 tail | bottleneck: Residual fixed-shape overhead in the generic tail kernel, especially generic control flow and narrower export/store handling rather than hot-band feed mechanics.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
