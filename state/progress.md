# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1db08fc0e373507cd63d0a43e4791f43c6de5b17`
- plateau counter: `101`
- round loop: `round 10/100`
- rounds remaining: `91`
- notes: `Node C is ready to implement diagnosis_20260421_124005:dir_01 via recommended selection for round 10/100.`

## Latest measured custom run

- run id: `20260421_123908_bf16_gemm_v1_1db08fc`
- run dir: `runs/20260421_123908_bf16_gemm_v1_1db08fc`
- correctness: `PASS`
- median runtime: `46.056448 ms`
- TFLOP/s: `15.785399 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_124005`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/100 diagnosis emitted after the compact writer sweep stayed correctness-safe but failed to move the 198-register anchor.`
- dir_01: Retime the PTX barrier seam on the current correctness-safe 128x128 anchor | bottleneck: synchronization_barrier_issue layered on top of occupancy_latency_hiding_issue in the current correctness-safe 128x128 PTX anchor
- dir_02: Apply only a minimal PTX export-address cleanup on the correct anchor | bottleneck: occupancy_latency_hiding_issue with a small tail_overhead_or_generic_path_issue in the PTX export address math
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue attacked through geometry and register-budget change rather than another PTX-local cleanup

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
