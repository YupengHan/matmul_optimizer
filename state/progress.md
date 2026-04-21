# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `aaf076e228985145a4fa9736167899e6c710d1be`
- plateau counter: `97`
- round loop: `round 6/100`
- rounds remaining: `95`
- notes: `Node C is ready to implement diagnosis_20260421_114852:dir_01 via recommended selection for round 6/100.`

## Latest measured custom run

- run id: `20260421_114455_bf16_gemm_v1_aaf076e`
- run dir: `runs/20260421_114455_bf16_gemm_v1_aaf076e`
- correctness: `PASS`
- median runtime: `46.532095 ms`
- TFLOP/s: `15.624042 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_114852`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-review reflection for round 6: accept the live barrier-trim family and the PTX export cleanup family against the latest rich NCU evidence; defer the 256x128 register-budget transplant as the orthogonal structural branch; reject another accepted-surface restore this round because the current workload no longer reproduces the stale 24 ms anchor.`
- dir_01: Retime the PTX wait-group and CTA barrier seam on the current 128x128 anchor | bottleneck: synchronization_barrier_issue layered on top of an occupancy_latency_hiding_issue in the active 128x128 PTX hot-band kernel
- dir_02: Trim PTX export-address and store-path scalar live state after the MMA loop | bottleneck: occupancy_latency_hiding_issue with tail_overhead_or_generic_path_issue concentrated in the PTX export/store path
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue addressed by a geometry and register-budget change rather than another PTX-local retime

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
