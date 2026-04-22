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
- latest measured commit: `8fd88cb415da428b274f41325006b803a7f795ae`
- plateau counter: `29`
- round loop: `round 13/20`
- rounds remaining: `8`
- notes: `Node C build succeeded for round 13/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_192024_bf16_gemm_v1_8fd88cb4`
- run dir: `runs/20260421_192024_bf16_gemm_v1_8fd88cb4`
- correctness: `PASS`
- median runtime: `24.693696 ms`
- TFLOP/s: `29.441499 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_192105`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/20 diagnosis emitted from the restored compact PTX anchor; frontier should now prefer compact-surface sync experiments over any new geometry branch.`
- dir_01: Collapse The Compact PTX Wait-Sync Seam Into A Pairwise Stage Advance | bottleneck: Barrier and long-scoreboard are the clearest remaining compact-surface bottlenecks on the restored anchor.
- dir_02: Trim The Compact PTX Wait Group And Sync Cadence Without Growing Shared Memory | bottleneck: Barrier handoff overhead is still large enough to justify a smaller cadence-only probe on the compact PTX surface.
- dir_03: Keep The 2-K-Stage Pg2s Port Parked Behind The Compact Sync Experiments | bottleneck: If revisited later, the target is still compact-surface latency hiding and copy cadence, not a new geometry surface.

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
