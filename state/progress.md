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
- latest measured commit: `d7576a6e1833a4cb5fc914851ee6b2512930cb04`
- plateau counter: `13`
- round loop: `round 9/10`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 9/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_160001_bf16_gemm_v1_d7576a6e`
- run dir: `runs/20260421_160001_bf16_gemm_v1_d7576a6e`
- correctness: `PASS`
- median runtime: `26.730480 ms`
- TFLOP/s: `27.198143 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_160019`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 9: the current accepted-base family has now cleanly isolated the synchronization problem. That means the right next move is not another occupancy or export-lifetime theory; it is one final barrier/handoff retime on the current non-PTX 3-CTA surface. If that fails, the family should be closed and the final round can move to the broader 256x128 branch.`
- dir_01: Retime The Non-PTX 3-CTA Barrier/Handoff Seam | bottleneck: Barrier cadence and future-tile refill ordering on the non-PTX 3-CTA grouped-row hot-band kernel.
- dir_02: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: Wait-group release, barrier cadence, and refill ordering on the PTX 128x128 anchor without extra scratch growth.
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
