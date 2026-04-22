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
- latest measured commit: `1f02b14706466fc384b8bc6441be63e222670bba`
- plateau counter: `20`
- round loop: `round 4/20`
- rounds remaining: `17`
- notes: `Node C build succeeded for round 4/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_182631_bf16_gemm_v1_1f02b147`
- run dir: `runs/20260421_182631_bf16_gemm_v1_1f02b147`
- correctness: `PASS`
- median runtime: `25.063408 ms`
- TFLOP/s: `29.007205 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_182858`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4 treats 1f02b147 as the new accepted local PTX anchor. The next directions should exploit that recovery instead of replaying the exact register-interleave fingerprint that already failed and regressed.`
- dir_01: Deepen The Active PTX Hot-Band To A 3-Stage Pg2s Pipeline | bottleneck: Global-to-shared latency hiding at low occupancy: long_scoreboard 5.45% and mio_throttle 3.98% indicate cp.async completion is still arriving too late for the current two-stage PTX pipeline.
- dir_02: Split The Final PTX Wait/Sync Drain Out Of The Steady-State Loop | bottleneck: Residual barrier tax from the final no-refill handoff inside the PTX steady-state loop.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling On The Dominant Surface | bottleneck: Hot-band tiling and warp-level reuse ceiling: the 128x128 PTX surface may simply have run out of occupancy and locality headroom.

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
