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
- latest measured commit: `5383596d7276d7daebbe92c3dc04bea84a505aac`
- plateau counter: `3`
- round loop: `round 3/10`
- rounds remaining: `8`
- notes: `Node C is ready to implement diagnosis_20260421_145629_round03_5383596d:dir_01 via recommended selection for round 3/10.`

## Latest measured custom run

- run id: `20260421_145629_bf16_gemm_v1_5383596d`
- run dir: `runs/20260421_145629_bf16_gemm_v1_5383596d`
- correctness: `PASS`
- median runtime: `47.290880 ms`
- TFLOP/s: `15.373354 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_145629_round03_5383596d`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 should return to the accepted base run 20260421_133418_bf16_gemm_v1_c859cd06 before implementing any new direction. The 64x384 row-band expansion family is now explicitly deprioritized after the 47.291 ms regression.`
- dir_01: Restore The Accepted Base And Increase PTX Grouped-Row Depth | bottleneck: launch-order and B-tile reuse inefficiency inside the accepted PTX hot-band traversal
- dir_02: Restore The Accepted Base And Swap To The Single-K 128x128 Sibling | bottleneck: microkernel-specific accumulate ordering is contributing to scoreboard overhead on the accepted hot-band split
- dir_03: Restore The Accepted Base And Tighten PTX Launch Bounds | bottleneck: register pressure and low CTA residency on the accepted PTX hot-band path

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.289920 ms`
- current best custom gap vs cuBLAS: `1.874352 ms`, `1.084090x` of cuBLAS runtime (slower)
