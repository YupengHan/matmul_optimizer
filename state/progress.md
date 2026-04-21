# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2267a72bf3f325b7e4a3d2055eb54cdfb3326d6d`
- plateau counter: `27`
- round loop: `round 40/100`
- rounds remaining: `61`
- notes: `Node C is ready to implement diagnosis_20260421_082315:dir_01 via recommended selection for round 40/100.`

## Latest measured custom run

- run id: `20260421_082034_bf16_gemm_v1_2267a72`
- run dir: `runs/20260421_082034_bf16_gemm_v1_2267a72`
- correctness: `PASS`
- median runtime: `24.206848 ms`
- TFLOP/s: `30.033626 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_082315`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 40 restores the accepted PTX anchor first, then keeps the 256x128 pivot and grouped-rows=8 consumer-ordering surfaces live for the post-checkpoint queue.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Source drift away from the accepted PTX hot-band steady state after a measured-loss reopen, not DRAM saturation and not an immediate need for another same-family micro-retime.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Structural latency hiding and register/shared-memory amortization on the hot band, not another tiny PTX-local ordering tweak.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the already-closed wait/commit-window retime family.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
