# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5ae2249d5b7a8c9f9686021e82e20d1a24aa3bde`
- plateau counter: `0`
- round loop: `round 25/50`
- rounds remaining: `26`
- notes: `Node C build succeeded for round 25/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_001545_bf16_gemm_v1_5ae2249`
- run dir: `runs/20260420_001545_bf16_gemm_v1_5ae2249`
- correctness: `PASS`
- median runtime: `27.691520 ms`
- TFLOP/s: `26.254226 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001618`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 25: Register Reuse / compiler guidance is promoted again because the mild launch-bounds clue produced the largest single-round gain in this recent stretch, while the grouped-order L2 tuning has already identified a strong base at grouped_rows=8. L2 Cache remains accepted and now effectively baked into the base branch. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background infrastructure. Tiling 256x128 stays rejected, and aggressive launch-bounds remains rejected, but the measured 2-CTA regime makes `launch_bounds(128, 2)` the next sensible refinement.`
- dir_01: Keep grouped_rows=8 and refine the compiler clue to a two-argument launch-bounds target of 2 resident CTAs | bottleneck: Compiler allocation / instruction scheduling quality on the accepted grouped-order hot-band kernel, now that the preferred 2-CTA regime is visible in measured data.
- dir_02: Keep the new best grouped-order base unchanged and return to conservative barrier-side cleanup | bottleneck: Residual barrier overhead under the new best grouped-order + launch-bounds base.
- dir_03: Freeze the current best branch and revisit a neighboring grouped-order value only if compiler refinement stalls | bottleneck: Fine-grained L2-order tuning around the current best base.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.773631 ms`, `1.068433x` slower than CUTLASS
