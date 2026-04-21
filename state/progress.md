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
- latest measured commit: `9cac32cbd567419bdc7204b46a812665da0cc865`
- plateau counter: `11`
- round loop: `round 7/10`
- rounds remaining: `4`
- notes: `Node C build succeeded for round 7/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_155210_bf16_gemm_v1_9cac32cb`
- run dir: `runs/20260421_155210_bf16_gemm_v1_9cac32cb`
- correctness: `PASS`
- median runtime: `24.346112 ms`
- TFLOP/s: `29.861828 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_155253`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 7: the latest run validated the choice to leave the losing 256x128 surface, but it did not validate staying on the PTX family as the main branch. The recovered PTX run became a good fallback surface, not the new winner. That is why the ranking now prefers the accepted non-PTX sibling plus one bounded occupancy probe, keeps one PTX wait/sync-collapse refinement in reserve, and leaves the 256x128 family queued rather than deleting it.`
- dir_01: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the accepted non-PTX 128x128 hot-band surface.
- dir_02: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: The seam between cp.async wait-group release, __syncthreads(), and future-stage refill ordering on the PTX 128x128 microkernel.
- dir_03: Reopen The 256x128 Half-Panel Register-Reuse Branch Later | bottleneck: Register reuse, fragment lifetime, and writer-ownership constraints on the correctness-safe 256x128 pivot.

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
