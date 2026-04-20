# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b42811cb8dad2d5f208f388d8aea982b97a2c62e`
- plateau counter: `15`
- round loop: `round 16/50`
- rounds remaining: `35`
- notes: `Node C build succeeded for round 16/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_233546_bf16_gemm_v1_b42811c`
- run dir: `runs/20260419_233546_bf16_gemm_v1_b42811c`
- correctness: `FAIL`
- median runtime: `28.363264 ms`
- TFLOP/s: `25.632431 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_235321`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 16: accepted as primary for this round are Async Copy, Pg2s, Ps2r, Data Reuse, and Stage because the new 128x128 family already proved the macro shape and exposed a stage-reuse race. Deferred are Coalescing Access and Bank Conflict because the failing 28.36 ms run showed low mio-throttle and low scoreboard pressure, so feed width and bank fixes are not the immediate limiter. Register Reuse is also deferred because the 128x128 family already lifted tensor active materially without a new register scheme. The L2 cache / block-order clue stays alive as a later experiment, but only after the hot-band branch is correct.`
- dir_01: Make the 128x128 hot-band stage reuse safe before the next cp.async overwrite | bottleneck: Barrier / stage orchestration inside the hot-band mainloop. The goal is to trade a controlled barrier increase for removing the hidden producer-consumer race while preserving the much higher tensor utilization of the 128x128 branch.
- dir_02: Reintroduce the 128x128x32 steady-state once the 128x128 family is correct | bottleneck: Pipeline depth and control overhead in the hot-band kernel. This targets stage efficiency rather than a new macro tile.
- dir_03: Add an L2-friendly block-order clue only after the hot-band kernel is correct and stable | bottleneck: L2 reuse / CTA launch order rather than shared-memory feed. This is a compiler-scheduling clue experiment, not a first-order correctness or tensor-pipeline fix.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
