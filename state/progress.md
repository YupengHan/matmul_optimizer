# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6557fa0df424fb14ba776782e32b35635c89bbc0`
- plateau counter: `4`
- round loop: `round 5/50`
- rounds remaining: `46`
- notes: `Node C build succeeded for round 5/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_225440_bf16_gemm_v1_6557fa0`
- run dir: `runs/20260419_225440_bf16_gemm_v1_6557fa0`
- correctness: `FAIL`
- median runtime: `30.008207 ms`
- TFLOP/s: `24.227353 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_225521`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/50 starts from an incorrect but materially faster steady-state peel: the main 256x128 hot-band kernel improved by roughly 0.7 ms and tensor activity rose, but all correctness cases failed. That makes dir_01 the clear recommendation: preserve the peeled steady-state core and repair correctness by restoring the original final-two-tile handoff. Dir_02 carries the warp-local Ps2r/register-reuse human-idea branch if the peel cannot be repaired cleanly, and dir_03 keeps the lighter L2-friendly CTA swizzle as the cache-locality branch.`
- dir_01: Keep the peeled steady state, but restore the proven final-two-tile handoff to recover correctness | bottleneck: Correctness break in the final cp.async stage handoff of the peeled hot-band schedule, not a failure of the hot-band steady-state peeling idea itself.
- dir_02: Return to the accepted-correct surface and push warp-local Ps2r plus right-left register reuse | bottleneck: Per-warp operand delivery and short-scoreboard pressure inside the 64x64 PTX hot-band microkernel.
- dir_03: Try a lighter L2-friendly logical CTA swizzle over the hot-band grid | bottleneck: Inter-CTA L2 locality across the hot-band grid rather than per-warp compute scheduling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
