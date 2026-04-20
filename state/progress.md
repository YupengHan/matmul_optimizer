# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3be0a8e0196710b8fd1d015ae234bbd27af1a0ff`
- plateau counter: `10`
- round loop: `round 5/10`
- rounds remaining: `6`
- notes: `Node C build succeeded for round 5/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_210303_bf16_gemm_v1_3be0a8e`
- run dir: `runs/20260419_210303_bf16_gemm_v1_3be0a8e`
- correctness: `PASS`
- median runtime: `30.594048 ms`
- TFLOP/s: `23.763426 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_210642`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5 human-idea audit against the restored correct branch: Tiling is accepted and already embodied by the active 256x128 CTA / 64x64 warp hot kernel, so this round does not reopen macro shape; Coalescing Access is accepted as baseline because 16-byte cp.async staging is already in place; Data Reuse is accepted as baseline because the correct branch already relies on shared reuse for both operands; Async Copy is accepted as baseline for the same reason; Bank Conflict is accepted as the primary family for this round because the branch is correct again and the user explicitly asked for warp-local consumer-side work with no CTA repack; L2 Cache is deferred because the profile is not L2-bound; Register Reuse is accepted only in the user's internal-tile-order sense for this round, not in the half-panel sense, because the half-panel branch stayed unstable; Pg2s remains baseline because double-buffered global-to-shared staging is already present; Ps2r is accepted as a secondary family, but ranked below the lower-risk issue-order retune; Stage is accepted as a valid backup direction in fixed-shape control form. Recommended direction dir_01 therefore keeps the correct branch and applies the user's Right Left Right Left internal ordering idea directly to the hot kernel's B-consumer / MMA issue order.`
- dir_01: Human idea 5/7 Bank conflict + internal-tile order: keep the correct 256x128 hot kernel, but change the 64x64 warp-consumer order to Right/Left/Right/Left | bottleneck: Warp-local B-consumer delivery and internal fragment issue order on the true hot-band kernel. A win should show up as slightly higher tensor active and lower hot-band time without changing shared memory footprint or stage depth.
- dir_02: Human idea 10 Stage: specialize the fixed 452-tile hot loop into clearer prologue / steady-state / epilogue control | bottleneck: Generic loop-control and stage-transition overhead in the hot-band kernel rather than operand layout.
- dir_03: Human idea 9 Ps2r: add one-fragment shared-to-register lookahead inside the correct full-width 64x64 sweep | bottleneck: Warp-local shared-to-register feed latency inside the full-width hot-band sweep.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
