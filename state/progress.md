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
- latest measured commit: `ac1299d7d6b0b67e7eb323da7621c4511e79d6d8`
- plateau counter: `35`
- round loop: `round 19/20`
- rounds remaining: `2`
- notes: `Node C is ready to implement diagnosis_20260421_194601:dir_01 via frontier selection for round 19/20.`

## Latest measured custom run

- run id: `20260421_194414_bf16_gemm_v1_ac1299d7`
- run dir: `runs/20260421_194414_bf16_gemm_v1_ac1299d7`
- correctness: `PASS`
- median runtime: `24.688641 ms`
- TFLOP/s: `29.447527 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_194601`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19/20 diagnosis emitted from the restored clean compact PTX anchor; frontier should probe the PTX launch-bounds target before the loop closes.`
- dir_01: Retune The Clean Compact PTX Launch Bounds To Target Three-CTA Residency | bottleneck: Register-pressure-driven CTA residency remains the cleanest unresolved local bottleneck on the restored compact PTX surface.
- dir_02: Restore The Two-CTA Clean Compact PTX Anchor If The Launch-Bounds Probe Loses | bottleneck: The fallback issue would be a failed register-budget probe rather than a new algorithmic bottleneck.
- dir_03: Keep The Compact Barrier-Trim Family Parked Behind The Launch-Bounds Probe | bottleneck: Residual synchronization cost on the compact PTX loop, but with weaker marginal evidence than the register-pressure lever.

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
