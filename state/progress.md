# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7864f5515778a7b40f754bd5cb6ac6e0ec083ef2`
- plateau counter: `2`
- round loop: `round 30/50`
- rounds remaining: `21`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 30/50.`

## Latest measured custom run

- run id: `20260420_002455_bf16_gemm_v1_7864f55`
- run dir: `runs/20260420_002455_bf16_gemm_v1_7864f55`
- correctness: `PASS`
- median runtime: `30.668673 ms`
- TFLOP/s: `23.705604 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_002530`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 30: Register Reuse / compiler scheduling remains primary because the winning branch is still moving on small compiler-guided loop-scheduling changes. L2 Cache remains accepted and fixed at grouped_rows=8. Stage remains accepted as background structure, but K32 is again rejected even under the newer base conditions. Tiling 256x128, aggressive launch-bounds, peeled scheduling, and K32 are all now rejected for the current search state.`
- dir_01: Restore the current best grouped K16 branch and test the intermediate unroll factor between 2 and 4 | bottleneck: Loop-control / scheduling overhead in the current best hot-band K16 kernel, with the unroll factor now being the only moving part.
- dir_02: Keep the current best hot-band branch fixed and begin trimming the smaller non-hot-band remainder only if unroll-3 stalls | bottleneck: Secondary-region overhead after hot-band optimization saturates.
- dir_03: Freeze the current best branch and revisit tiny barrier-side cleanup only after the unroll midpoint result is known | bottleneck: Residual barrier overhead in the grouped K16 winner.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
