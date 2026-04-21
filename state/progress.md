# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `51883111c43f99e355df0f6612e2fa9a2a4af320`
- plateau counter: `6`
- round loop: `round 19/100`
- rounds remaining: `82`
- notes: `Node C build succeeded for round 19/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_003148_bf16_gemm_v1_5188311`
- run dir: `runs/20260421_003148_bf16_gemm_v1_5188311`
- correctness: `PASS`
- median runtime: `24.534016 ms`
- TFLOP/s: `29.633120 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_003229`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19 treats grouped_rows=8 as clear negative evidence. The next move is a direct restore back to the PTX winner surface, while 256x128 pivot and the non-PTX 128x128 sibling remain live as the next two alternate families.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: The grouped_rows=8 locality regime itself is the measured problem here; the immediate need is to remove that drift and recover the proven PTX winner surface.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path rather than PTX grouped-row locality.
- dir_03: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: CTA traversal and locality on the non-PTX 128x128 sibling surface rather than PTX microkernel control behavior.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
