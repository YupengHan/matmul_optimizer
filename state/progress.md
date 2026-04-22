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
- latest measured commit: `117cd3e796a5742c1f15e040edf78cb668e1d5cf`
- plateau counter: `17`
- round loop: `round 1/20`
- rounds remaining: `20`
- notes: `Node C build succeeded for round 1/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_172601_bf16_gemm_v1_117cd3e7`
- run dir: `runs/20260421_172601_bf16_gemm_v1_117cd3e7`
- correctness: `PASS`
- median runtime: `24.806945 ms`
- TFLOP/s: `29.307092 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_175153`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/20 maps the persistent guidance explicitly: register reuse stays primary, tiling stays alive but deferred, and deeper async-copy staging is deferred because the staged 128x128 family already regressed while the current run is still first-order register/occupancy bound.`
- dir_01: Swap The Recovered PTX Hot-Band Back To The Regular 128x128 Single-K Sibling | bottleneck: Microkernel-specific consume ordering and residual accumulator live range on the dominant 128x128 hot-band path are still holding occupancy to the 2-CTA class.
- dir_02: Retune The PTX Hot-Band Launch Bounds For Three-CTA Residency | bottleneck: Register-pressure-driven CTA residency cap on the current PTX hot-band microkernel.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Family After The PTX Recovery | bottleneck: Hot-band tiling and panel-reuse ceiling on the current 128x128 surface rather than pure bandwidth or tail overhead.

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
