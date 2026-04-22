# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f42c93101ebc1d8ce622165a216d68ff55b0839e`
- plateau counter: `34`
- round loop: `round 18/20`
- rounds remaining: `3`
- notes: `Node C is ready to implement diagnosis_20260421_194243:dir_01 via frontier selection for round 18/20.`

## Latest measured custom run

- run id: `20260421_194145_bf16_gemm_v1_f42c9310`
- run dir: `runs/20260421_194145_bf16_gemm_v1_f42c9310`
- correctness: `PASS`
- median runtime: `24.881616 ms`
- TFLOP/s: `29.219140 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_194243`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 18/20 diagnosis emitted from the partial x32 recovery run; frontier should restore the true compact PTX wait-sync anchor before any further exploration.`
- dir_01: Restore The Clean Compact PTX Wait-Sync Anchor After The Partial X32 Recovery | bottleneck: The immediate issue is a residual sync-seam regression inside the compact PTX loop, not a broader occupancy or staging family choice.
- dir_02: Resume Compact Sync-Family Tuning Only After The Clean Anchor Returns | bottleneck: Residual barrier overhead on the true compact PTX anchor after the seam restore.
- dir_03: Keep The Existing X32 Staged Family Closed Until Its Footprint Drops Materially | bottleneck: Occupancy and latency hiding would still dominate any reopen of the current staged family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `frontier`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
