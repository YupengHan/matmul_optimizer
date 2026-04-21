# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4c6e7a1bac5778edccc11a1267e301c1a0d37401`
- plateau counter: `14`
- round loop: `round 27/100`
- rounds remaining: `74`
- notes: `Node C build succeeded for round 27/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_011620_bf16_gemm_v1_4c6e7a1`
- run dir: `runs/20260421_011620_bf16_gemm_v1_4c6e7a1`
- correctness: `PASS`
- median runtime: `24.183295 ms`
- TFLOP/s: `30.062877 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_011652`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 27 interprets the non-PTX sibling as a correct plateau alternate, not as a new leader. The ranking therefore re-centers the exact PTX winner while keeping the sibling and grouped_rows=8 surfaces alive as lower-ranked alternate states.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the best measured correct surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.
- dir_03: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the exact same surface restore targeted by dir_01.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
