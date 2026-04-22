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
- latest measured commit: `434ded2afbec179fb9d82954d80903a4907fc5e5`
- plateau counter: `24`
- round loop: `round 8/20`
- rounds remaining: `13`
- notes: `Node C build succeeded for round 8/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_185050_bf16_gemm_v1_434ded2a`
- run dir: `runs/20260421_185050_bf16_gemm_v1_434ded2a`
- correctness: `PASS`
- median runtime: `25.461216 ms`
- TFLOP/s: `28.553995 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_185158`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8 diagnosis emitted after the compact two-stage grouped_rows=2 retest recovered registers but reintroduced a large long_scoreboard penalty.`
- dir_01: Restore Grouped Rows From 2 Back To 4 On The Compact Two-Stage PTX Ring | bottleneck: Long-scoreboard pressure from the grouped_rows=2 launch order is now the most specific local bottleneck to remove.
- dir_02: Trim The Compact Two-Stage PTX Wait-Sync Cadence Without Growing Shared Memory | bottleneck: Barrier and CTA handoff overhead are the likely next bottlenecks after grouped_rows is restored.
- dir_03: Reopen The 256x128 64x64-Warp Hot-Band Branch From The Compact PTX Base | bottleneck: The 128x128 PTX surface may still be occupancy-limited by geometry and warp reuse even after local launch-order cleanup.

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
