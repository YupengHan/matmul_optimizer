# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Fixed 64x96 Tail On The Restored 1181247 Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_190757`
- round loop: `round 10/50`
- hypothesis: `The human-review queue still contains only workflow state and no new user-supplied idea bullets, so round 10 has to make the accept/defer/reject mapping directly from the measured evidence. The latest measured run cc89c17 rejected the peeled-single-stage residual family as the default next move because end-to-end performance regressed from 24.422464 ms to 25.152928 ms even though the hot-band kernel stayed essentially unchanged and the peeled kernel looked better in isolation. On that regressed run, the fixed 64x96 tail is now the clearest remaining bounded outlier: it still consumes about 0.908 ms while showing the worst stall mix in the profile at 26.14% barrier, 15.59% long-scoreboard, 13.50% short-scoreboard, and 14.66% MIO throttle. Since the implementation surface is already restored to the accepted 1181247 base, the best next move is to leave the main hot-band and peeled default alone and trim the isolated tail path.`
- expected bottleneck: `Generic 64x96 tail staging and epilogue synchronization overhead on the restored fixed split.`
- code locations: `src/kernels/bf16_gemm_v1.cu:40-78, src/kernels/bf16_gemm_v1.cu:1167-1178, src/kernels/bf16_gemm_v1.cu:1298-1405, src/kernels/bf16_gemm_v1.cu:2130-2136`
- risk: `Low to moderate. The tail path is isolated and the current source is already back on the accepted base, but the tail is a sub-millisecond kernel so the upside is bounded and easy to lose in noise if the edit leaks into generic paths.`
- metrics to re-check: `end-to-end median runtime versus the 24.422464 ms 1181247 baseline, p10 and p90 runtime spread on the fixed perf run, 64x96 tail kernel gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct for the tail kernel, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct for the tail kernel, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct for the tail kernel, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct for the tail kernel`

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
