# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `466263fcce7c61689773fa9fec22144a0d7233e1`
- plateau counter: `14`
- round loop: `round 15/50`
- rounds remaining: `36`
- notes: `Node C build succeeded for round 15/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_233123_bf16_gemm_v1_466263f`
- run dir: `runs/20260419_233123_bf16_gemm_v1_466263f`
- correctness: `FAIL`
- median runtime: `29.493760 ms`
- TFLOP/s: `24.649940 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_233204`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/50 keeps the new 128x128 family alive because it delivered the first major kernel-time improvement in many rounds. The recommended next move is a localization step: preserve the winning CTA/launch shape and revert only the K32 mainloop to K16 so the correctness bug can be isolated without discarding the structural gain.`
- dir_01: Keep the 128x128/128-thread hot-band branch but revert only the K32 mainloop back to proven K16 staging to localize correctness | bottleneck: Correctness bug likely in the K32 staged mainloop bookkeeping, not in the new 128x128 warp mapping.
- dir_02: If 128x128 K16 is correct, reintroduce K32 with explicit [stage][half] helpers to eliminate half-stage aliasing | bottleneck: Stage-half address aliasing or refill ordering inside the new K32 mainloop.
- dir_03: Restore the accepted-correct implementation surface if the new family cannot be made correct quickly | bottleneck: Not a bottleneck attack; this is the fallback path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
