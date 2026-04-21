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
- latest measured commit: `7496aff21c8de79011caa26978ba7dd249179f64`
- plateau counter: `6`
- round loop: `round 2/10`
- rounds remaining: `9`
- notes: `Node C build succeeded for round 2/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_150910_bf16_gemm_v1_7496aff2`
- run dir: `runs/20260421_150910_bf16_gemm_v1_7496aff2`
- correctness: `PASS`
- median runtime: `24.537088 ms`
- TFLOP/s: `29.629409 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_150910_round02_clean_7496aff2`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis continues the clean 10-round loop. The 8-row grouped setting is now treated as a measured negative result, so the next recommended clean round moves to the non-microkernel sibling.`
- dir_01: Swap To The Single-K 128x128 Non-Microkernel Sibling | bottleneck: microkernel-specific accumulate ordering is contributing to long-scoreboard stalls on the accepted hot-band split
- dir_02: Retune PTX Launch Bounds On The Clean Baseline | bottleneck: register pressure and low CTA residency on the accepted PTX hot-band path
- dir_03: Try A Shallower PTX Grouped-Row Setting | bottleneck: current grouped-row traversal may still be mismatched to A/B locality balance on the accepted PTX hot-band path

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
