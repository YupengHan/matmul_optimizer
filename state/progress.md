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
- latest measured commit: `05086a14f8df006f564c0071ea7d60dbf5ddc156`
- plateau counter: `18`
- round loop: `round 2/20`
- rounds remaining: `19`
- notes: `Node C is ready to implement diagnosis_20260421_175735:dir_01 via recommended selection for round 2/20.`

## Latest measured custom run

- run id: `20260421_175700_bf16_gemm_v1_05086a14`
- run dir: `runs/20260421_175700_bf16_gemm_v1_05086a14`
- correctness: `PASS`
- median runtime: `26.385408 ms`
- TFLOP/s: `27.553844 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_175735`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2 treats the regular 128x128 sibling as a measured_loss for accepted-base promotion: it improved occupancy and long-scoreboard locally, but the barrier / short-scoreboard regression dominated total runtime. The next moves all restore the compact PTX surface first and then change one lever at a time.`
- dir_01: Restore The Compact PTX Hot-Band And Retest Three-CTA Residency There | bottleneck: The accepted compact PTX surface is still register-limited, but the beneficial part of the current regression may be the 3-CTA residency rather than the sibling kernel body.
- dir_02: Restore The Compact PTX Hot-Band And Trim Barrier Cadence Without Shared-Memory Blowup | bottleneck: Single-K barrier cadence and CTA handoff overhead on the accepted compact PTX hot-band surface remain the unresolved latency tax once the row-pair live-range reset is in place.
- dir_03: Restore The Compact PTX Hot-Band And Try Grouped Rows Equals Two | bottleneck: The accepted PTX grouped-row traversal may still be mismatched to the A/B locality balance on the fixed hot-band surface.

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
