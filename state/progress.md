# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ba8c2d77c1b0b705e48783da6d9dc73105d16707`
- plateau counter: `25`
- round loop: `round 38/100`
- rounds remaining: `63`
- notes: `Node C is ready to implement diagnosis_20260421_082719:dir_01 via recommended selection for round 38/100.`

## Latest measured custom run

- run id: `20260421_075613_bf16_gemm_v1_ba8c2d7`
- run dir: `runs/20260421_075613_bf16_gemm_v1_ba8c2d7`
- correctness: `PASS`
- median runtime: `24.184272 ms`
- TFLOP/s: `30.061663 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_082719`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 38 uses restore-first ranking to recover the accepted PTX anchor before reopening the next PTX control-path retime or the structural 256x128 pivot.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the accepted PTX hot-band steady state, not DRAM saturation and not another immediate structural pivot.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual cp.async wait-group timing and inner-loop control cadence in the PTX 128x128 hot-band microkernel after the restore anchor is back in place.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Structural latency hiding and register/shared-memory amortization on the hot band, not one more tiny PTX-local ordering tweak.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
