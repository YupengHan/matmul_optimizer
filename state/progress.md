# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `11df0f1f1b3949e13d33e59024c9de95c414f134`
- plateau counter: `3`
- round loop: `round 11/100`
- rounds remaining: `90`
- notes: `Node C is ready to implement diagnosis_20260420_233235:dir_01 via recommended selection for round 11/100.`

## Latest measured custom run

- run id: `20260420_233034_bf16_gemm_v1_11df0f1`
- run dir: `runs/20260420_233034_bf16_gemm_v1_11df0f1`
- correctness: `PASS`
- median runtime: `24.190464 ms`
- TFLOP/s: `30.053968 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_233235`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/100 audit: round 10 exposed a search-memory hygiene issue that the loop now has to account for explicitly. The nominally top-ranked sibling export-trim family is already absorbed in the current source, so repeating it would only create a fake node_c round; after switching to an approved PTX control fallback, the latest measured run still regressed to 24.19046402 ms while the headline signature stayed effectively unchanged at 16.61 active warps, 5.46 barrier, and 7.24 long-scoreboard. This diagnosis therefore filters absorbed or already-baked families out of the top ranks and reorders only the still-actionable current-source deltas. The recommendation moves to the steady-state barrier/handoff retime because it is the strongest open frontier family that is both unabsorbed and still aligned with the latest flat scheduler signature.`
- dir_01: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the handoff between the current stage's MMA issue and the future-tile refill sequence.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel, especially around the grouped CTA mapping and export-handoff behavior.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid rather than another inner-loop scheduler issue.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753536 ms`, `0.932343x` slower than CUTLASS
