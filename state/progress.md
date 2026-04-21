# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `20cad7985754ff930f5e7d06a9f6e08152a2635b`
- plateau counter: `15`
- round loop: `round 28/100`
- rounds remaining: `73`
- notes: `Node C build succeeded for round 28/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_011816_bf16_gemm_v1_20cad79`
- run dir: `runs/20260421_011816_bf16_gemm_v1_20cad79`
- correctness: `PASS`
- median runtime: `24.167423 ms`
- TFLOP/s: `30.082620 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_012002`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 28 explicitly treats both the exact PTX winner and the non-PTX sibling as plateau anchors. The main search budget shifts to one clean recheck of grouped_rows=8 so the loop can either validate or close that alternate PTX surface with fresh evidence.`
- dir_01: Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the already-replayed exact PTX restore and not another same-plateau alternate-surface A/B.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact recovery path back to the strongest measured anchor.
- dir_03: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
