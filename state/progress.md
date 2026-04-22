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
- latest measured commit: `823cbff48af806c5e9c80a6da9ea7087ef3c459b`
- plateau counter: `25`
- round loop: `round 9/20`
- rounds remaining: `12`
- notes: `Node C build succeeded for round 9/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- run dir: `runs/20260421_185710_bf16_gemm_v1_823cbff4`
- correctness: `PASS`
- median runtime: `24.697857 ms`
- TFLOP/s: `29.436539 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_185824`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9 diagnosis emitted from the new compact PTX accepted base after grouped_rows restoration.`
- dir_01: Trim The Compact Two-Stage PTX Wait-Sync Cadence On The 22016B Shared Surface | bottleneck: Barrier and CTA handoff overhead are the clearest remaining local bottlenecks on the accepted compact PTX base.
- dir_02: Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop | bottleneck: Warp-local shared-pointer arithmetic and hot-loop control overhead are small but still relevant on the accepted compact PTX base.
- dir_03: Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Current PTX Base | bottleneck: The 128x128 PTX surface may still be capped by occupancy and warp-reuse geometry even after local loop cleanup.

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
