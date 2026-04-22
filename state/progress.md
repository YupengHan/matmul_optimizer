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
- latest measured commit: `88a8acfc6a0c4389f714a79adad71b17558c09a6`
- plateau counter: `27`
- round loop: `round 11/20`
- rounds remaining: `10`
- notes: `Node C is ready to implement diagnosis_20260421_191121:dir_01 via frontier selection for round 11/20.`

## Latest measured custom run

- run id: `20260421_190652_bf16_gemm_v1_88a8acfc`
- run dir: `runs/20260421_190652_bf16_gemm_v1_88a8acfc`
- correctness: `PASS`
- median runtime: `24.689153 ms`
- TFLOP/s: `29.446917 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_191121`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/20 diagnosis emitted from the live 24.689153 ms compact PTX plateau; frontier should prefer a structural branch over stale restore-base replay.`
- dir_01: Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Current Compact PTX Base | bottleneck: The dominant ceiling is occupancy and hot-band geometry on the active 128x128 PTX path, not raw DRAM bandwidth.
- dir_02: Port The 2-K-Stage Pg2s Schedule Onto The Active 128x128 PTX Microkernel | bottleneck: The active PTX hot-band path is still limited by per-tile Pg2s cadence and the resulting latency-hiding gap.
- dir_03: Reopen Pairwise Wait-Sync Collapse On The Current Compact PTX Surface | bottleneck: The remaining bottleneck on the compact PTX surface is hot-loop synchronization cadence rather than address setup.

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
