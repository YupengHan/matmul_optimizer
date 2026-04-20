# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b4f4a28d3f4f13c71f287127a37f5fe71a5b930c`
- plateau counter: `1`
- round loop: `round 27/50`
- rounds remaining: `24`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 27/50.`

## Latest measured custom run

- run id: `20260420_001930_bf16_gemm_v1_b4f4a28`
- run dir: `runs/20260420_001930_bf16_gemm_v1_b4f4a28`
- correctness: `PASS`
- median runtime: `31.002625 ms`
- TFLOP/s: `23.450254 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_002004`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 27: Stage remains relevant, but after the failed peeled rewrite the right interpretation is now 'reduce control overhead gently' rather than 'rewrite the loop schedule.' Register Reuse / compiler guidance also remains active because the best branch still relies on grouped L2 ordering plus `launch_bounds(128, 2)`. L2 Cache stays accepted and fixed at grouped_rows=8. Tiling 256x128, aggressive launch-bounds, and the peeled schedule are now rejected on measured evidence. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Restore the current best branch and raise the hot-band K16 loop from unroll-1 to a small fixed unroll factor | bottleneck: Loop-control overhead in the accepted hot-band K16 kernel, approached through milder compiler unrolling rather than manual schedule peeling.
- dir_02: Restore the current best branch unchanged and revisit tiny barrier-side cleanup only if unrolling stalls | bottleneck: Residual barrier overhead under the grouped_rows=8 plus `launch_bounds(128, 2)` base.
- dir_03: Freeze the current best branch and revisit a neighboring compiler clue only after the unroll result is known | bottleneck: Compiler codegen refinement on the current best branch.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.309376 ms`, `1.050520x` slower than CUTLASS
