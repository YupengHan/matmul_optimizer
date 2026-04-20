# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c26ac4fdc00ad89cefc324b30d4fc8758fb4d0af`
- plateau counter: `0`
- round loop: `round 28/50`
- rounds remaining: `23`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 28/50.`

## Latest measured custom run

- run id: `20260420_002119_bf16_gemm_v1_c26ac4f`
- run dir: `runs/20260420_002119_bf16_gemm_v1_c26ac4f`
- correctness: `PASS`
- median runtime: `27.022336 ms`
- TFLOP/s: `26.904388 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_002144`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 28: Register Reuse / compiler scheduling remains the primary family because grouped ordering and `launch_bounds(128, 2)` are already fixed into the base, and the first unroll increase produced another large measured gain. L2 Cache stays accepted and fixed at grouped_rows=8. Stage remains accepted as background structure but is no longer the first lever to perturb. Tiling 256x128, aggressive launch-bounds, and the peeled schedule remain rejected.`
- dir_01: Keep the current best branch and raise the hot-band K16 loop to the next small unroll factor | bottleneck: Residual loop-control and scheduling overhead in the current best hot-band K16 kernel.
- dir_02: Freeze the current best branch and revisit one more mild compiler clue only if higher unrolling stalls | bottleneck: Compiler codegen refinement on the grouped_rows=8 plus `launch_bounds(128, 2)` base.
- dir_03: Hold the current best branch fixed and return to tiny barrier-side cleanup only if compiler tuning saturates | bottleneck: Residual barrier overhead in the current best hot-band kernel.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
