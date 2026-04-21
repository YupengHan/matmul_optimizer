# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `910beff68055b974cfdbb268cda1087c8b44d665`
- plateau counter: `9`
- round loop: `round 22/100`
- rounds remaining: `79`
- notes: `Node C is ready to implement diagnosis_20260421_005324:dir_01 via recommended selection for round 22/100.`

## Latest measured custom run

- run id: `20260421_005058_bf16_gemm_v1_910beff`
- run dir: `runs/20260421_005058_bf16_gemm_v1_910beff`
- correctness: `PASS`
- median runtime: `24.178688 ms`
- TFLOP/s: `30.068605 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_005324`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 22 treats the round-21 sibling run as a plateau-equivalent alternate surface, not as a new frontier leader. The current correct surfaces are all clustered within 0.02 ms and keep the same 16.6%-warps / 48%-tensor machine state, so the next recommendation intentionally shifts to the only historical family that ever broke that wall: the half-panel 256x128 register-reuse branch.`
- dir_01: Repair The 256x128 Half-Panel Register-Reuse Branch | bottleneck: Register-limited occupancy and oversized live state on the wide hot-band family, which the plateaued PTX and sibling surfaces are no longer moving.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is an exact recovery of the best-known implementation surface.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Hot-band K-loop scheduling and latency hiding on a broader 256x128 reuse regime rather than the live-state wall on the plateaued 128x128 surfaces.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
