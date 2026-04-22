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
- latest measured commit: `fd0092669df3780c996e69e2f2236614caa3d2ec`
- plateau counter: `33`
- round loop: `round 17/20`
- rounds remaining: `4`
- notes: `Node C is ready to implement diagnosis_20260421_193904:dir_01 via frontier selection for round 17/20.`

## Latest measured custom run

- run id: `20260421_193649_bf16_gemm_v1_fd009266`
- run dir: `runs/20260421_193649_bf16_gemm_v1_fd009266`
- correctness: `PASS`
- median runtime: `31.612928 ms`
- TFLOP/s: `22.997535 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_193904`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17/20 diagnosis emitted from the failed existing 128x128x32 staged-kernel probe; frontier should restore the accepted compact PTX anchor before any further search.`
- dir_01: Restore The Accepted Compact PTX Anchor After The Failed Existing X32 Probe | bottleneck: The immediate bottleneck is not an unresolved compact-surface seam; it is the residency and sync damage introduced by the x32 staged probe.
- dir_02: Reopen Compact Barrier Trims Only After The Anchor Is Back | bottleneck: Residual barrier overhead on the compact PTX surface after the broken x32 branch is removed.
- dir_03: Only Revisit X32 Staging If Its Register And Shared-Memory Footprint Is Cut Materially | bottleneck: Occupancy and latency hiding would remain the dominant failure mode unless the staged kernel's resident footprint is reduced substantially.

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
