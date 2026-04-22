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
- latest measured commit: `40488b6e7f3a41519a2cc1af8152e45b02857870`
- plateau counter: `30`
- round loop: `round 14/20`
- rounds remaining: `7`
- notes: `Node C is ready to implement diagnosis_20260421_192742:dir_01 via frontier selection for round 14/20.`

## Latest measured custom run

- run id: `20260421_192654_bf16_gemm_v1_40488b6e`
- run dir: `runs/20260421_192654_bf16_gemm_v1_40488b6e`
- correctness: `PASS`
- median runtime: `24.845312 ms`
- TFLOP/s: `29.261835 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_192742`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/20 diagnosis emitted from a second compact-surface wait_sync_collapse loss; frontier should restore the clean compact seam before trying another family.`
- dir_01: Restore The Compact Two-Stage PTX Anchor After The Failed Wait-Sync-Collapse Variant | bottleneck: The immediate problem is the regressing wait_sync_collapse variant itself, which raised barrier and registers on the active compact surface.
- dir_02: Retry The Narrow Compact PTX Cadence Trim After Restoring The Anchor | bottleneck: Barrier remains the clearest unresolved compact-surface stall once the failed wait_sync_collapse variant is unwound.
- dir_03: Keep The Guarded 2-K-Stage Pg2s Port As The Third Compact-Anchor Fallback | bottleneck: If revisited later, the target remains latency hiding on the compact PTX surface rather than another wide-tiling change.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `frontier`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
