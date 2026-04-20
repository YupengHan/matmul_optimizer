# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `797c137cc3c66a42beb82a28e0e8e5010cb2f59b`
- plateau counter: `3`
- round loop: `round 4/50`
- rounds remaining: `47`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 4/50.`

## Latest measured custom run

- run id: `20260419_224922_bf16_gemm_v1_797c137`
- run dir: `runs/20260419_224922_bf16_gemm_v1_797c137`
- correctness: `PASS`
- median runtime: `30.461472 ms`
- TFLOP/s: `23.866852 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_224955`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/50 starts from a run where the dedicated residual 64x128 PTX kernel helped the last 64 rows, but the dominant 256x128 hot-band kernel remained effectively unchanged relative to the accepted base. The recommended next move is therefore dir_01: keep the new shared 64x64 PTX family, but peel the fixed 452-tile steady state so the compiler sees an exact prologue / steady-state / epilogue schedule. Dir_02 keeps pressure inside warp-local Ps2r/register reuse, and dir_03 holds the lighter L2-swizzle idea as a lower-ranked cache-locality branch.`
- dir_01: Peel the 452-tile steady state for the shared 64x64 PTX hot-band family | bottleneck: Hot-band control/orchestration overhead inside the fixed-shape PTX main loop, which is still diluting tensor issue after the residual path was specialized.
- dir_02: Push warp-local Ps2r and register-reuse scheduling inside the 64x64 PTX microkernel | bottleneck: Per-warp operand delivery and short-scoreboard pressure inside the hot-band MMA loop rather than CTA-level shared-memory staging.
- dir_03: Try a light L2-friendly CTA swizzle over the 60x25 hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band B tiles rather than per-CTA tensor scheduling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
