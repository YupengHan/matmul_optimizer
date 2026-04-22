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
- latest measured commit: `097581913eed49b85bf1043f45e2d165485732b1`
- plateau counter: `31`
- round loop: `round 15/20`
- rounds remaining: `6`
- notes: `Node C is ready to implement diagnosis_20260421_193031:dir_01 via frontier selection for round 15/20.`

## Latest measured custom run

- run id: `20260421_192933_bf16_gemm_v1_09758191`
- run dir: `runs/20260421_192933_bf16_gemm_v1_09758191`
- correctness: `PASS`
- median runtime: `24.682431 ms`
- TFLOP/s: `29.454936 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_193031`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/20 diagnosis emitted from the current accepted compact PTX base; frontier should try the smallest final-drain barrier trim before the checkpoint.`
- dir_01: Skip The Final No-Refill CTA Sync On The Compact PTX Anchor | bottleneck: The remaining local tax is unnecessary final-drain barrier overhead on the accepted compact PTX surface.
- dir_02: Keep The Guarded 2-K-Stage Pg2s Port As The Broader Fallback | bottleneck: If revisited later, the target remains compact-surface latency hiding and per-tile copy cadence.
- dir_03: Leave The Wait-Sync-Collapse Family Parked Behind Smaller Compact Tweaks | bottleneck: If revisited later, the target would again be the compact loop's wait/refill seam, but not before smaller barrier trims flatten out.

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
