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
- latest measured commit: `5ea07e356339f761e5361611762dceb0273a84b6`
- plateau counter: `2`
- round loop: `round 2/10`
- rounds remaining: `9`
- notes: `Restore-base reset the implementation surface to run_id=20260421_133418_bf16_gemm_v1_c859cd06.`

## Latest measured custom run

- run id: `20260421_142317_bf16_gemm_v1_5ea07e35`
- run dir: `runs/20260421_142317_bf16_gemm_v1_5ea07e35`
- correctness: `PASS`
- median runtime: `30.007680 ms`
- TFLOP/s: `24.227778 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_142317_round02_5ea07e35`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 should branch from the accepted base run 20260421_133418_bf16_gemm_v1_c859cd06, not from the round-1 regressed staged-kernel head. The top priority is to reduce time spent in the 128x128 hotspot rather than add more K-stage depth there.`
- dir_01: Restore The Accepted Base And Expand The 64x384 Row Band | bottleneck: too much of the fixed hot band is assigned to the 128x128 PTX hotspot instead of the stronger 64x384 family
- dir_02: Retune PTX Hot-Band Grouped-Row Traversal | bottleneck: launch-order and cache/locality inefficiency inside the accepted PTX hot-band traversal
- dir_03: Swap To The Single-K 128x128 Non-Microkernel Sibling | bottleneck: microkernel-specific accumulate/store scheduling inside the accepted 128x128 hot-band path

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
