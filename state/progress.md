# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5bbcf7bf12808e0ed5168a9dcd5ac93c81d2c65c`
- plateau counter: `32`
- round loop: `round 16/20`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 16/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_193214_bf16_gemm_v1_5bbcf7bf`
- run dir: `runs/20260421_193214_bf16_gemm_v1_5bbcf7bf`
- correctness: `PASS`
- median runtime: `24.882688 ms`
- TFLOP/s: `29.217882 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_193427`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16/20 diagnosis emitted from the post-checkpoint compact anchor regression; frontier should try the existing 128x128x32 staged kernel before spending more rounds on tiny compact seam trims.`
- dir_01: Promote The Existing 128x128x32 Two-K-Stage Hot-Band Kernel From The Clean Compact Anchor | bottleneck: The unresolved bottleneck is still latency hiding and copy/sync amortization on the accepted compact surface, not a new geometry family.
- dir_02: Restore The Accepted Compact PTX Anchor If The Broader Staged Probe Loses | bottleneck: The immediate fallback problem would be a failed staged-kernel branch rather than a fresh compact-surface bottleneck.
- dir_03: Leave The Tiny Compact Sync Tweaks Parked Behind The Broader Staged Probe | bottleneck: If revisited later, the target would still be residual barrier overhead on the compact anchor, but not before the staged probe is measured.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `frontier`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
