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
- latest measured commit: `d51419e68ece25d501edff44e937b6f56053d97c`
- plateau counter: `23`
- round loop: `round 7/20`
- rounds remaining: `14`
- notes: `Node C build succeeded for round 7/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- run dir: `runs/20260421_184622_bf16_gemm_v1_d51419e6`
- correctness: `PASS`
- median runtime: `28.767664 ms`
- TFLOP/s: `25.272105 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_184831`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7 diagnosis emitted from live reasoning after the round-6 drain-split regression.`
- dir_01: Restore A Compact Two-Stage PTX Ring While Keeping Grouped Rows At 2 | bottleneck: Registers-per-thread and occupancy are the first bottlenecks to remove; barrier cleanup is no longer the primary limiter after the round-6 regression.
- dir_02: Restore The Known Two-Stage PTX Anchor With Grouped Rows Back At 4 | bottleneck: This is a restore family aimed at removing register and occupancy damage rather than discovering a new local bottleneck.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Branch After Resetting Register Pressure | bottleneck: The 128x128 PTX surface may still be capped by geometry and warp-reuse limits even after register cleanup.

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
