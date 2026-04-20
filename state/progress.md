# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1cc244fde41bb83706b3bc4840740c9715b54c41`
- plateau counter: `11`
- round loop: `round 12/50`
- rounds remaining: `39`
- notes: `Node C build succeeded for round 12/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_231544_bf16_gemm_v1_1cc244f`
- run dir: `runs/20260419_231544_bf16_gemm_v1_1cc244f`
- correctness: `PASS`
- median runtime: `31.758848 ms`
- TFLOP/s: `22.891870 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_231606`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/50 absorbs a strong negative result from the half-CTA Pg2s experiment. The hot-band kernel regressed badly, so the next staging-family move should deepen overlap by reallocating shared-memory budget instead of reducing the number of copy-issuing threads. The untried secondary family remains a consumer-side B swizzle that does not add CTA-level repacking.`
- dir_01: Restore the accepted-correct hot-band surface and trade paired c_shared scratch for a 3-stage A/B pipeline | bottleneck: Tensor under-utilization from a too-shallow hot-band mainloop pipeline rather than pure DRAM bandwidth.
- dir_02: Restore the accepted surface and try a light consumer-side B XOR/interleaved swizzle with no extra shared footprint | bottleneck: Shared-memory bank behavior and operand delivery on the hot-band B consumer path.
- dir_03: Restore the accepted-correct implementation surface before any new experiment | bottleneck: Not a bottleneck attack; this is the reset path that preserves signal quality for later rounds.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
