# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `abefa1e9a75ebf02bf1674afd4045d40e3195784`
- plateau counter: `7`
- round loop: `round 8/50`
- rounds remaining: `43`
- notes: `Node C build succeeded for round 8/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_230410_bf16_gemm_v1_abefa1e`
- run dir: `runs/20260419_230410_bf16_gemm_v1_abefa1e`
- correctness: `PASS`
- median runtime: `30.550528 ms`
- TFLOP/s: `23.797279 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_230527`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/50 resets the search: the current correct branch is materially slower than the accepted best implementation, and several recent rounds have mixed correctness/debug work with forward optimization. The recommended next move is therefore dir_01, a clean restore to commit 0d78758. Dir_02 and dir_03 then capture the next two human-idea branches to try on that restored surface: deeper A-side Ps2r and a lighter L2-friendly CTA swizzle.`
- dir_01: Re-anchor exactly at the accepted best implementation commit 0d78758 before more experiments | bottleneck: Not a bottleneck attack. This is a reset to the fastest correct implementation surface before the next human-idea experiments.
- dir_02: On the restored surface, try A-side Ps2r row-pair lookahead inside the 64x64 PTX microkernel | bottleneck: Warp-local shared-to-register latency on the A-side of the 64x64 PTX hot-band microkernel.
- dir_03: On the restored surface, test a light L2-friendly logical CTA swizzle on the hot-band grid | bottleneck: Inter-CTA L2 locality across neighboring hot-band tiles.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
