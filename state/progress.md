# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a64efcefb5aa9f2ef5ba3ba7a606cdf018c384bd`
- plateau counter: `8`
- round loop: `round 21/100`
- rounds remaining: `80`
- notes: `Node C is ready to implement diagnosis_20260421_003952:dir_01 via recommended selection for round 21/100.`

## Latest measured custom run

- run id: `20260421_003751_bf16_gemm_v1_a64efce`
- run dir: `runs/20260421_003751_bf16_gemm_v1_a64efce`
- correctness: `PASS`
- median runtime: `30.136320 ms`
- TFLOP/s: `24.124360 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_003952`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 21 treats round 20 as a hard negative on the exact 256x128 pivot promotion, not as a reason to retreat into more PTX-local noise chasing. The new ranking therefore promotes the closest evidence-backed alternate surface, keeps the exact PTX restore as the low-risk recovery fallback, and rehydrates one historical high-ceiling half-panel family back into the live queue so the search does not stay trapped inside 24.16-24.18 ms micro-variance.`
- dir_01: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: PTX-microkernel-specific control/export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: The round-20 regression is dominated by the bad 256x128 pivot surface itself, so the restore attacks source drift rather than a live machine bottleneck family.
- dir_03: Repair The 256x128 Half-Panel Register-Reuse Branch With Compact B Staging | bottleneck: Register-limited occupancy and oversized live state on the wide hot-band family, with the real fix requiring end-to-end half-panel staging rather than only half-width accumulation.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
