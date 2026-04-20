# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `be44358062dd87db8692cf1a8ce8017bab55a65d`
- plateau counter: `0`
- round loop: `round 17/50`
- rounds remaining: `34`
- notes: `Node C build succeeded for round 17/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_235558_bf16_gemm_v1_be44358`
- run dir: `runs/20260419_235558_bf16_gemm_v1_be44358`
- correctness: `PASS`
- median runtime: `29.204992 ms`
- TFLOP/s: `24.893669 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_235645`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 17: accepted as primary are Stage, Async Copy, Pg2s, Ps2r, and Data Reuse because the corrected 128x128 path established that orchestration, not macro tiling, is what unlocked the new best custom runtime. Tiling 256x128 with 64x64 warp tiles is deferred because the 128x128 family has not yet been fully exploited and already beats the prior best custom result. Coalescing Access and Bank Conflict are deferred again because mio-throttle and scoreboard pressure are not the dominant signals in the corrected run. Register Reuse is also deferred because the current gain came from stage timing rather than a new register schedule. The L2 cache / block-order clue remains a valid later experiment, but only after the hot-band pipeline is stable.`
- dir_01: Re-enable the 128x128x32 hot-band steady-state with the proven consume-before-overwrite fence | bottleneck: Mainloop control and overlap efficiency in the corrected 128x128 family. The target is to raise tensor active back toward the earlier incorrect K32/K16 peaks without reopening the shared-stage race.
- dir_02: Tighten the K16 consume fence instead of fencing every iteration with a full CTA barrier | bottleneck: Barrier overhead inside the corrected K16 mainloop rather than memory bandwidth or a macro-tile limitation.
- dir_03: Try an L2-friendly CTA-order clue only after the corrected hot-band pipeline stabilizes | bottleneck: L2 reuse and block-issue locality rather than tensor-core delivery within a CTA.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.287104 ms`, `1.126828x` slower than CUTLASS
