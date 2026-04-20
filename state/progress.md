# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1e8ffddc0cd1587cdd1fd9b6403d24f57c24cc45`
- plateau counter: `3`
- round loop: `round 31/50`
- rounds remaining: `20`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 31/50.`

## Latest measured custom run

- run id: `20260420_002629_bf16_gemm_v1_1e8ffdd`
- run dir: `runs/20260420_002629_bf16_gemm_v1_1e8ffdd`
- correctness: `PASS`
- median runtime: `27.601408 ms`
- TFLOP/s: `26.339940 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_002707`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 31: L2 Cache is promoted again, but specifically because the branch conditions changed after the original grouped-order sweep. The current best branch now combines grouped ordering, `launch_bounds(128, 2)`, and unroll-2, so re-checking the nearby grouped setting is more justified than repeating unrelated hot-band ideas. Register Reuse and compiler guidance remain accepted in the background because they define the current base. K32, peeled scheduling, aggressive launch-bounds, and 256x128 remain rejected.`
- dir_01: Restore the current best branch and re-test grouped_rows=4 under the newer launch-bounds plus unroll-2 codegen | bottleneck: Cross-CTA locality under the newer compiler-guided hot-band branch, not under the earlier baseline used in the first grouped-order sweep.
- dir_02: Freeze the current best hot-band branch and start trimming the smaller non-hot-band remainder only if the grouped re-check is neutral | bottleneck: Secondary-region overhead outside the main hot band.
- dir_03: Hold the current best branch fixed and revisit tiny barrier-side cleanup only after the grouped re-check is settled | bottleneck: Residual barrier overhead in the current best hot-band kernel.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
