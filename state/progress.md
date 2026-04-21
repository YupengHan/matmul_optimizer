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
- latest measured commit: `f1c576ee202b38cd0287e625e807069c95525f77`
- plateau counter: `9`
- round loop: `round 5/10`
- rounds remaining: `6`
- notes: `Node C build succeeded for round 5/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_153357_bf16_gemm_v1_f1c576ee`
- run dir: `runs/20260421_153357_bf16_gemm_v1_f1c576ee`
- correctness: `PASS`
- median runtime: `30.173615 ms`
- TFLOP/s: `24.094541 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_153357_round05_clean_f1c576ee`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5 human-guidance review: Tiling(accept but reject simple 256x128 promotion), Coalescing Access(guardrail, already present), Data Reuse(accept), Async Copy(guardrail, already present), Bank Conflict(accept), L2 Cache(accept as secondary), Register Reuse(strong accept), Pg2s(accept), Ps2r(accept), Stage(accept but reject shared-memory blowup). The simple 256x128 pivot is now treated as a measured negative; only deeper 256x128 salvage or bounded occupancy probes stay active.`
- dir_01: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint, stage design, and reuse efficiency inside the 256x128 hot-band path are still the missing pieces preventing the human-guided tiling family from becoming viable.
- dir_02: Force 3-CTA Residency On The Non-PTX 128x128 Sibling | bottleneck: Register-limited occupancy and latency hiding on the current non-PTX 128x128 accepted surface.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the lower shared-memory footprint.

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
