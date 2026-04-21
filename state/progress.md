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
- latest measured commit: `6cc462c46b05712b972773911a1a7f31892ddcb2`
- plateau counter: `5`
- round loop: `round 1/10`
- rounds remaining: `10`
- notes: `Node C build succeeded for round 1/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_150626_bf16_gemm_v1_6cc462c4`
- run dir: `runs/20260421_150626_bf16_gemm_v1_6cc462c4`
- correctness: `PASS`
- median runtime: `24.323521 ms`
- TFLOP/s: `29.889564 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_150626_round01_clean_6cc462c4`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis starts the fresh clean 10-round loop. The earlier contaminated absolute timings are excluded from ranking except as weak structural hints.`
- dir_01: Increase PTX Grouped-Row Depth On The Clean Baseline | bottleneck: launch-order and B-tile reuse inefficiency inside the accepted PTX hot-band traversal
- dir_02: Swap To The Single-K 128x128 Non-Microkernel Sibling | bottleneck: microkernel-specific accumulate ordering is contributing to scoreboard overhead on the accepted hot-band split
- dir_03: Retune PTX Launch Bounds As A Fallback | bottleneck: register pressure and low CTA residency on the accepted PTX hot-band path

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
