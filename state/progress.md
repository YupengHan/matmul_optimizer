# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `273d63c0dca706eb94e279d165295463933a4b5c`
- plateau counter: `0`
- round loop: `round 22/50`
- rounds remaining: `29`
- notes: `Node C build succeeded for round 22/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_001122_bf16_gemm_v1_273d63c`
- run dir: `runs/20260420_001122_bf16_gemm_v1_273d63c`
- correctness: `PASS`
- median runtime: `28.949504 ms`
- TFLOP/s: `25.113364 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001157`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 22: L2 Cache remains the primary family because it just produced the best custom runtime so far without perturbing the working CTA-local pipeline. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted fixed infrastructure rather than the next tuning knob. Register Reuse is still deferred after the launch-bounds failure. Tiling 256x128 stays rejected on measured evidence. Coalescing Access and Bank Conflict remain deferred because the current improvement signal came from CTA ordering, not those metrics.`
- dir_01: Keep the grouped CTA-order remap and increase the hot-band row-group size to deepen B-tile reuse | bottleneck: Cross-CTA B reuse / L2 locality rather than CTA-local staging or occupancy.
- dir_02: Keep the grouped-order remap but reduce the row-group size to check whether the current win is already over-grouped | bottleneck: Cache-locality tuning of the grouped CTA traversal.
- dir_03: Hold the grouped-order base fixed and return to conservative K16 barrier trimming | bottleneck: Residual barrier overhead inside the accepted grouped-order K16 kernel.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.031615 ms`, `1.116970x` slower than CUTLASS
