# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2d59c53bd4db8d90980c6e5a9a70f09c8dda482b`
- plateau counter: `13`
- round loop: `round 26/100`
- rounds remaining: `75`
- notes: `Node C is ready to implement diagnosis_20260421_011427:dir_01 via recommended selection for round 26/100.`

## Latest measured custom run

- run id: `20260421_011200_bf16_gemm_v1_2d59c53`
- run dir: `runs/20260421_011200_bf16_gemm_v1_2d59c53`
- correctness: `PASS`
- median runtime: `24.690687 ms`
- TFLOP/s: `29.445087 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_011427`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 26 treats round 25 as a clear negative on the auxiliary 256x128 structural probe. The ranking now returns to correctness-proven alternate surfaces rather than spending another round on a closed geometry family or a frozen PTX micro-retime family.`
- dir_01: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the best measured correct surface.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the same surface restore targeted by dir_02.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
