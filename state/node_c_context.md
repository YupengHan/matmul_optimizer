# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep The Exact Current Base And Tighten The One-Sync Handoff`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_105103`
- round loop: `round 70/100`
- hypothesis: `Round 69 restored the implementation surface in src/kernels/bf16_gemm_v1.cu back to the historical round-58 accepted commit, with only semantically equivalent future_tile_k arithmetic or comment shape left different, and it still measured 25.49913597 ms. That means the currently reproducible exact base in this environment is about 25.50 ms, not the historical 24.57 ms snapshot. On that exact base, the remaining visibly material stall is barrier at 6.41, while long_scoreboard is already down to 3.98 and mio to 3.21. The next highest-value open family is therefore a very narrow one-sync handoff closure on the exact current base: keep grouped_rows=8, the right-left 64x64 PTX consume order, reversed PTX compute row-pair traversal, linear export traversal, B-first refill, active-loop unroll 2, accepted 256x128 unroll 1, and accepted helper shapes fixed, and only tighten the wait_group_0 plus __syncthreads handoff around the future-tile refill without reopening fixed-K peeling, A-first refill, K32 cadence, or extra-live staging.`
- expected bottleneck: `Residual synchronization overhead in the active PTX hot-band steady-state handoff. The exact-base profile is no longer dominated by export-lifetime or large scoreboard effects, but barrier is still materially above the old round-58 snapshot, making the current one-sync handoff the best open synchronization-family target.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1961 B-first prologue staging in the active PTX kernel, src/kernels/bf16_gemm_v1.cu:1977 active PTX hot-band loop with unroll 2, src/kernels/bf16_gemm_v1.cu:1994 exact-base one-sync handoff with cp_async_wait_group_0 and __syncthreads, src/kernels/bf16_gemm_v1.cu:1998 B-first future-tile refill path on the exact current base`
- risk: `Medium. This direction becomes bad if it drifts into any already-closed family: fixed-K peeling, deeper staging, A-first refill, extra-live lookahead, or K32 cadence. The implementation boundary must stay very narrow and preserve the accepted base semantics.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
