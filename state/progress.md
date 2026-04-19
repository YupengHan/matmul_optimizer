# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `56038948d7d255701cbdaf6c5969d0fbc56b4aa7`
- plateau counter: `2`
- round loop: `round 8/20`
- rounds remaining: `13`
- notes: `Node C build succeeded for round 8/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_232047_bf16_gemm_v1_5603894`
- run dir: `runs/20260418_232047_bf16_gemm_v1_5603894`
- correctness: `PASS`
- median runtime: `54.193089 ms`
- TFLOP/s: `13.415353 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_232136`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Specialize the fixed-shape K loop so the 4-warp CTA spends less time in barrier and control overhead | bottleneck: Synchronization and hot-path control overhead in the double-buffered async-copy pipeline
- dir_02: Refine the same-footprint B shared layout so three `matrix_b` loads hit a friendlier per-warp pattern | bottleneck: Shared-memory B fragment load pressure and MIO saturation in the steady-state tensor loop
- dir_03: Attack the `c_shared` epilogue so the kernel sheds shared-memory footprint and MIO-heavy writeback work | bottleneck: Epilogue LSU/MIO pressure and shared-memory residency headroom lost to `c_shared`

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `28.219023 ms`, `2.088786x` slower than CUTLASS
