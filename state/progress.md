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
- latest measured commit: `257c9662ad79d8c40a9bd26f43d72ce39dc978f6`
- plateau counter: `36`
- round loop: `round 20/20`
- rounds remaining: `1`
- notes: `Node C build succeeded for round 20/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_194813_bf16_gemm_v1_257c9662`
- run dir: `runs/20260421_194813_bf16_gemm_v1_257c9662`
- correctness: `PASS`
- median runtime: `26.079727 ms`
- TFLOP/s: `27.876803 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_194853`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 20/20 diagnosis emitted from the failed 3-CTA PTX launch-bounds probe; frontier should restore the clean compact PTX anchor to close the loop.`
- dir_01: Restore The Clean Compact PTX Anchor After The Failed Three-CTA Probe | bottleneck: The immediate problem is a failed register-budget probe, not an unresolved algorithmic bottleneck.
- dir_02: Keep The Compact Barrier-Trim Family Parked After Its Earlier Losses | bottleneck: Residual synchronization cost on the compact PTX loop, but with weaker evidence than the immediate restore.
- dir_03: Keep The Existing X32 Staged Family Closed On This Branch End State | bottleneck: Occupancy and synchronization tradeoffs on the staged family remain structurally unfavorable.

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
