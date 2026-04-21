# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b79a9bff2c5466a7cdd23c591f7eda181f319daf`
- plateau counter: `98`
- round loop: `round 7/100`
- rounds remaining: `94`
- notes: `Node C is ready to implement diagnosis_20260421_122308:dir_01 via recommended selection for round 7/100.`

## Latest measured custom run

- run id: `20260421_122240_bf16_gemm_v1_b79a9bf`
- run dir: `runs/20260421_122240_bf16_gemm_v1_b79a9bf`
- correctness: `PASS`
- median runtime: `46.021631 ms`
- TFLOP/s: `15.797341 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_122308`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/100 diagnosis emitted after the round-6 helper-flattening probe improved runtime slightly without changing the core occupancy signature.`
- dir_01: Trim PTX export/store-path scalar live state on the current 128x128 anchor | bottleneck: occupancy_latency_hiding_issue with tail_overhead_or_generic_path_issue concentrated in the PTX export/store path after the MMA loop
- dir_02: Retime the PTX wait-group and CTA barrier seam on the current anchor | bottleneck: synchronization_barrier_issue layered on top of an occupancy_latency_hiding_issue in the active 128x128 PTX hot-band kernel
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue addressed by a geometry and register-budget change rather than another PTX-local retime

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
