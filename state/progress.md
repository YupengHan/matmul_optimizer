# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `7c672be6dd341dd11a21e8959d47bdd07a6acc39`
- plateau counter: `1`
- round loop: `round 29/50`
- rounds remaining: `22`
- notes: `Node C build succeeded for round 29/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_002230_bf16_gemm_v1_7c672be`
- run dir: `runs/20260420_002230_bf16_gemm_v1_7c672be`
- correctness: `PASS`
- median runtime: `29.662720 ms`
- TFLOP/s: `24.509533 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_002345`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 29: Stage is promoted again, but specifically as a re-evaluation of the K32 branch under the new grouped-order plus compiler-guided base. The earlier K32 rejection remains valid for the old regime, but the current best branch changed the occupancy/codegen picture enough that the comparison should be refreshed once. Register Reuse and L2 Cache remain accepted because the current best branch already depends on both. Tiling 256x128, aggressive launch-bounds, and the peeled schedule remain rejected.`
- dir_01: Revisit the 128x128x32 hot-band branch on top of the current grouped-order plus launch-bounds base | bottleneck: Stage-depth / control-overhead tradeoff under the new best branch conditions, not under the older pre-grouped baseline.
- dir_02: Keep the current best K16 branch fixed and revisit tiny barrier-side cleanup only if the K32 re-test fails again | bottleneck: Residual barrier overhead in the grouped-order plus launch-bounds K16 winner.
- dir_03: Freeze the current best hot-band branch and look at a small secondary-region optimization only after the K32 re-test result is known | bottleneck: Secondary-region overhead outside the main hot band.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `1.104447 ms`, `1.042613x` slower than CUTLASS
