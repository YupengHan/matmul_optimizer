# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `11f04271ca6d1544510b98163a61027d6cef8c5d`
- plateau counter: `0`
- round loop: `round 21/50`
- rounds remaining: `30`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 21/50.`

## Latest measured custom run

- run id: `20260420_000930_bf16_gemm_v1_11f0427`
- run dir: `runs/20260420_000930_bf16_gemm_v1_11f0427`
- correctness: `PASS`
- median runtime: `29.116928 ms`
- TFLOP/s: `24.968960 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_001011`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 21: L2 Cache is now promoted to the primary family because the accepted 128x128 K16 path has stabilized and the recent CTA-local experiments either regressed or delivered only tiny gains. Stage, Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted as the fixed pipeline under the current base rather than the next thing to perturb. Register Reuse is deferred after the round-19 launch-bounds failure. Tiling 256x128 remains rejected on measured evidence. Coalescing Access and Bank Conflict are still deferred because current wins and losses have not been driven mainly by those signals.`
- dir_01: Keep the accepted 128x128 K16 kernel and apply an L2-friendly grouped CTA order on the hot band | bottleneck: L2 / B-tile reuse across CTAs rather than within-CTA shared-memory orchestration.
- dir_02: Hold the accepted base fixed and continue shaving barrier work inside the K16 steady-state | bottleneck: Residual barrier overhead in the accepted K16 hot-band loop.
- dir_03: Revisit a mild compiler register hint only after the accepted base survives the L2 pass unchanged | bottleneck: Compiler allocation quality rather than CTA-local algorithm shape.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.199039 ms`, `1.123430x` slower than CUTLASS
