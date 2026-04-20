# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8a2834ad9966fb75ef7c310ad5850de8c925ec5e`
- plateau counter: `0`
- round loop: `round 26/50`
- rounds remaining: `25`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 26/50.`

## Latest measured custom run

- run id: `20260420_001707_bf16_gemm_v1_8a2834a`
- run dir: `runs/20260420_001707_bf16_gemm_v1_8a2834a`
- correctness: `PASS`
- median runtime: `27.227264 ms`
- TFLOP/s: `26.701890 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001749`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 26: Stage is promoted again, but now in the fixed-shape-steady-state sense rather than a deeper buffering sense. The current best branch already incorporates the accepted L2 Cache setting (`grouped_rows=8`) and the best measured compiler clue (`launch_bounds(128, 2)`), so the next rational move is to reduce control overhead in the fixed 452-tile K loop. Register Reuse remains accepted in the background because the best branch still depends on the compiler clue, but it is not the first thing to perturb this round. Tiling 256x128 and aggressive launch-bounds remain rejected. Coalescing Access and Bank Conflict remain deferred.`
- dir_01: Keep the current best branch and peel the fixed 452-tile K loop into steady-state plus epilogue | bottleneck: Mainloop control-flow and stage-transition overhead inside the accepted hot-band kernel.
- dir_02: Hold the current best branch fixed and return to tiny barrier-side cleanup only if peeling stalls | bottleneck: Residual barrier overhead under the current best grouped-order + launch-bounds(128,2) base.
- dir_03: Freeze the current best base and revisit one more moderate compiler clue only after the peeled schedule result is known | bottleneck: Compiler codegen refinement on top of the current best branch.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.309376 ms`, `1.050520x` slower than CUTLASS
