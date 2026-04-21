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
- latest measured commit: `83acaae48069fdc5202a8bddf7cc4120d9d2ac62`
- plateau counter: `12`
- round loop: `round 8/10`
- rounds remaining: `3`
- notes: `Node C is ready to implement diagnosis_20260421_155620:dir_01 via recommended selection for round 8/10.`

## Latest measured custom run

- run id: `20260421_155533_bf16_gemm_v1_83acaae4`
- run dir: `runs/20260421_155533_bf16_gemm_v1_83acaae4`
- correctness: `PASS`
- median runtime: `26.541056 ms`
- TFLOP/s: `27.392257 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_155620`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 8: the current loop still respects the user's 256x128/64x64 preference, but the latest negative result is not yet a clean reason to abandon the accepted-base family. The round-7 surface carried both 3-CTA residency and a two-stage export scratch lifetime, so the first priority is to separate those effects. That is why dir_01 trims export scratch first, dir_02 keeps a same-surface barrier retime in reserve, and the 256x128 family stays queued rather than selected immediately.`
- dir_01: Trim The Grouped-Row 128x128 Sibling Export Scratch To Single Stage | bottleneck: Shared export lifetime and barrier tax on the grouped-row non-PTX 128x128 sibling, currently confounded with the 3-CTA residency probe.
- dir_02: Retime The Non-PTX 3-CTA Barrier/Handoff Seam | bottleneck: Barrier cadence at the seam between cp.async wait completion, __syncthreads(), and future-tile refill ordering on the non-PTX 3-CTA sibling.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, B-fragment lifetime, and writer-ownership constraints on the correctness-safe 256x128 pivot.

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
