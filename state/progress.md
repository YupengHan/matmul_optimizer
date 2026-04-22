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
- latest measured commit: `c03bcd3afa5031aacad05eaa97d0f16ad55b6192`
- plateau counter: `22`
- round loop: `round 6/20`
- rounds remaining: `15`
- notes: `Node C is ready to implement diagnosis_20260421_184151:dir_01 via frontier selection for round 6/20.`

## Latest measured custom run

- run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- run dir: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a`
- correctness: `PASS`
- median runtime: `25.755136 ms`
- TFLOP/s: `28.228134 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_184151`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6 treats the grouped_rows=2 probe as a negative result on top of a still-informative 3-stage family. The next move should either fix the late drain or restore the clean two-stage PTX anchor before another broad branch jump.`
- dir_01: Split The Final 3-Stage PTX Drain Out Of The Late Steady-State Loop | bottleneck: Late-drain synchronization is now the clearest remaining local tax on the 3-stage PTX surface.
- dir_02: Restore The Two-Stage PTX Anchor After The 3-Stage Probes | bottleneck: This is a fallback restore family, not a new bottleneck theory: it resets the search to the cleanest recent PTX anchor so later branches can be tested from a lower-variance surface.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling On The Dominant Surface | bottleneck: The 128x128 PTX surface may still be hitting a real tiling and warp-reuse ceiling even after local pipeline cleanup.

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
