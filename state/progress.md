# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7f84649e4684d1f8f0c55953524757ca10af6d97`
- plateau counter: `2`
- round loop: `round 15/100`
- rounds remaining: `86`
- notes: `Node C is ready to implement diagnosis_20260421_000721:dir_01 via recommended selection for round 15/100.`

## Latest measured custom run

- run id: `20260421_000626_bf16_gemm_v1_7f84649`
- run dir: `runs/20260421_000626_bf16_gemm_v1_7f84649`
- correctness: `PASS`
- median runtime: `24.178592 ms`
- TFLOP/s: `30.068725 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_000721`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/100 audit: round 14 confirmed that the round-13 regression was a single bad handoff variant, not broader source drift. The current source matches the best-known `489574e` PTX kernel file again and recovered to the 24.16-24.18 ms performance band. That lets the diagnosis filter out absorbed restore/export families and the already-rejected A-then-B handoff, then return to the strongest genuinely open active-PTX follow-on while preserving one alternate PTX surface and one orthogonal round-history fallback in the live queue.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual control-path and consume-order overhead inside the active PTX hot-band microkernel after the absorbed restore/export cleanup and the rejected handoff variant are removed from consideration.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel under the grouped_rows=8 regime.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth and not another PTX grouped-row retime.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
