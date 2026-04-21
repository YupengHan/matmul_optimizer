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
- latest measured commit: `24f31aab56b50712067f744ffab280ba1e33c341`
- plateau counter: `8`
- round loop: `round 4/10`
- rounds remaining: `7`
- notes: `Node C build succeeded for round 4/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_153021_bf16_gemm_v1_24f31aab`
- run dir: `runs/20260421_153021_bf16_gemm_v1_24f31aab`
- correctness: `PASS`
- median runtime: `24.195072 ms`
- TFLOP/s: `30.048244 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_153021_round04_clean_24f31aab`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4 explicitly lets the persistent human guidance pull the ranking toward 256x128 families. The round-3 hoist win is accepted as a useful 128x128 cleanup, but it did not move occupancy or scoreboard enough to justify another small 128x128-only exploit first.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Current four-warp 128x128 CTA geometry is capping residency and CTA-count efficiency on the hot-band region more than local pointer arithmetic is.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path are still capping residency and latency hiding.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence and PTX-stage handoff overhead inside the single-K 128x128 microkernel remain an unresolved latency tax on the accepted PTX surface.

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
