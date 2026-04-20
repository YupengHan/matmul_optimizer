# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a80b5afb975ecc8cf7cdc1e21ce10496d4b0faf4`
- plateau counter: `9`
- round loop: `round 10/50`
- rounds remaining: `41`
- notes: `Node C build succeeded for round 10/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_230856_bf16_gemm_v1_a80b5af`
- run dir: `runs/20260419_230856_bf16_gemm_v1_a80b5af`
- correctness: `FAIL`
- median runtime: `30.431232 ms`
- TFLOP/s: `23.890568 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_230948`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/50 pivots away from warp-local fragment-residency experiments because they have been too fragile on correctness. The recommended next move is therefore dir_01: restore the accepted-correct surface and test a light L2-friendly CTA swizzle, which is the safest remaining human-idea branch with a plausible upside.`
- dir_01: Restore the accepted-correct surface and try a light 4-column serpentine CTA swizzle on the hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band B tiles rather than warp-local tensor scheduling.
- dir_02: Restore the accepted-correct surface and try warp-specialized Pg2s staging without changing the tile shape | bottleneck: CTA-level staging orchestration and barrier dilution inside the hot-band loop.
- dir_03: Restore-only fallback to the accepted best surface | bottleneck: Not a bottleneck attack; this is the fallback reset path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
