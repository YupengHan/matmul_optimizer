# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a471728dccf675859934e8afab163929c08171be`
- plateau counter: `5`
- round loop: `round 18/100`
- rounds remaining: `83`
- notes: `Node C build succeeded for round 18/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_002817_bf16_gemm_v1_a471728`
- run dir: `runs/20260421_002817_bf16_gemm_v1_a471728`
- correctness: `PASS`
- median runtime: `24.172960 ms`
- TFLOP/s: `30.075730 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_002857`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 18 treats the restore family as absorbed again: the source matches the PTX winner surface and runtime has returned to the 24.17 band. The next recommendation therefore moves to the strongest alternate live family, grouped_rows=8, while 256x128 pivot and the non-PTX 128x128 sibling remain in the diagnosis to preserve queue breadth after the search-policy reset.`
- dir_01: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer-order locality on the PTX hot-band microkernel, not the already-restored prologue/refill seam on the grouped_rows=4 winner surface.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path, not the current PTX control-path seam.
- dir_03: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: CTA traversal and locality on the non-PTX 128x128 sibling surface rather than PTX microkernel control-path behavior.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
