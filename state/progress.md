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
- latest measured commit: `404e8c4448f47b60c80ebe2bd49a351d12b73535`
- plateau counter: `14`
- round loop: `round 10/10`
- rounds remaining: `1`
- notes: `Node C is ready to implement diagnosis_20260421_160315:dir_01 via recommended selection for round 10/10.`

## Latest measured custom run

- run id: `20260421_160237_bf16_gemm_v1_404e8c44`
- run dir: `runs/20260421_160237_bf16_gemm_v1_404e8c44`
- correctness: `PASS`
- median runtime: `25.996288 ms`
- TFLOP/s: `27.966278 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_160315`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for round 10: the 256x128 branch remains the strategic high-ceiling family, but the accepted-base family already produced enough evidence that the final round is better spent on one last bounded near-base PTX synchronization probe. The non-PTX 3-CTA family is now sufficiently tested and should be treated as closed after this loop.`
- dir_01: Collapse PTX Wait-Group Handoff Without Extra Export Scratch | bottleneck: Wait-group release, barrier cadence, and refill ordering on the PTX 128x128 anchor without extra export-scratch growth.
- dir_02: Reopen The 256x128 Half-Panel Register-Reuse Branch | bottleneck: Register reuse, compact B staging, and half-panel export mapping on the 256x128 pivot branch.
- dir_03: Restore The Accepted Base If The Final Probe Fails | bottleneck: None. This is a state-restoration fallback, not a new performance hypothesis.

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
