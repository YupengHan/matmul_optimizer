# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6bee469ece2906ab9efdd498b44f9b8d05b6e1bc`
- plateau counter: `3`
- round loop: `round 9/20`
- rounds remaining: `12`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 9/20.`

## Latest measured custom run

- run id: `20260418_233053_bf16_gemm_v1_6bee469`
- run dir: `runs/20260418_233053_bf16_gemm_v1_6bee469`
- correctness: `PASS`
- median runtime: `56.870047 ms`
- TFLOP/s: `12.783872 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_233315`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9 intentionally includes substantial human-in-loop guidance and a more exploratory, out-of-box diagnosis mindset. Using docs/heuristics.md explicitly, the current profile reads as a mixed global-memory plus synchronization plus instruction-mix imbalance, not a small tail or prologue-cleanup problem; at 56.87 ms, the kernel is still far from the ~20 ms long-horizon ceiling, so the ranking favors structural changes over another incremental K-loop prologue/steady-state/drain tweak. Round 9 node_c should restore to the round-7 measured commit before applying the selected direction.`
- dir_01: Retile to a 64x96 CTA so each staged B tile feeds more MMA before the next sync | bottleneck: Global-memory and LSU-heavy instruction mix starving Tensor Cores; the current shared-limited 7-block residency caps the kernel near 28 active warps/SM and still leaves too little math per staged K slice.
- dir_02: Remove the shared-memory epilogue scratch and recover occupancy plus LSU budget for the steady state | bottleneck: Shared-memory footprint and epilogue LSU traffic are reinforcing the same MIO/LSU congestion seen in the profile and are blocking higher CTA residency even though registers are not the limiting resource.
- dir_03: Replace the lockstep double buffer with a more overlapped producer-consumer cp.async pipeline | bottleneck: Synchronization and MIO throttle inside the steady-state K loop; the current double-buffered design still executes as a block-wide phase machine rather than a truly overlapped pipeline.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `28.219023 ms`, `2.088786x` slower than CUTLASS
