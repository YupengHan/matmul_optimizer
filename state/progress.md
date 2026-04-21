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
- latest measured commit: `2fbb368dd19ae7df53b7f4dc6cee09c0a21666a4`
- plateau counter: `7`
- round loop: `round 3/10`
- rounds remaining: `8`
- notes: `Node C is ready to implement diagnosis_20260421_152228_round03_clean_2fbb368d:dir_01 via recommended selection for round 3/10.`

## Latest measured custom run

- run id: `20260421_152228_bf16_gemm_v1_2fbb368d`
- run dir: `runs/20260421_152228_bf16_gemm_v1_2fbb368d`
- correctness: `PASS`
- median runtime: `24.392608 ms`
- TFLOP/s: `29.804908 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_152228_round03_clean_2fbb368d`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 explicitly folds master heuristic-history families into the ranking. The just-measured non-microkernel sibling is treated as partial positive signal, not a new base: it improved the previous regressed run but still did not reclaim the clean accepted runtime. Persistent human guidance from state/human_guidance.md is now part of every frontier-search read set.`
- dir_01: Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop | bottleneck: Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are still diluting tensor issue on a latency-limited path.
- dir_02: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel is still interrupting the steady-state issue flow even on the smaller shared-memory footprint.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path are still capping residency and latency hiding on the current workload.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
