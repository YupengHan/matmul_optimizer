# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `803e7499227b26770fccecb4b6d03f4079a5f06c`
- plateau counter: `16`
- round loop: `round 29/100`
- rounds remaining: `72`
- notes: `Node C is ready to implement diagnosis_20260421_012211:dir_01 via recommended selection for round 29/100.`

## Latest measured custom run

- run id: `20260421_012143_bf16_gemm_v1_803e749`
- run dir: `runs/20260421_012143_bf16_gemm_v1_803e749`
- correctness: `PASS`
- median runtime: `24.517119 ms`
- TFLOP/s: `29.653542 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_012211`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 29 switches the ranking rule from local plateau chasing to structure-first search. On the latest measured run, the hot-band PTX kernel still dominates at about 32.69 us with 200 registers per thread, 22,016 B shared memory per block, occupancy limit registers=2, and only 16.59% active warps. DRAM is only 9.77%, so the bottleneck is not bandwidth. The search therefore treats the 24.16-24.18 ms cluster as a noise-band plateau and ranks directions by whether they can break the residency wall instead of whether they can replay another small control-path delta.`
- dir_01: Force 3-CTA Residency On The PTX 128x128 Hot Band | bottleneck: Register-limited occupancy and latency hiding in the 128x128 PTX hot-band kernel, not global bandwidth.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path, plus barrier overhead created by the old half-panel ownership split.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
