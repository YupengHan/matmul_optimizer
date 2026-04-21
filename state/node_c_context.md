# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The PTX 128x128 Hot-Band Control Branch On The Restored 1181247 Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_191417`
- round loop: `round 11/50`
- hypothesis: `The human-review queue still contains only workflow state and no new user-supplied idea bullets, so the ranking has to be explicit from the measured evidence. Round 11 rejects the tail-only family as the next default move because the latest measured run 69f60e6 still regressed to 25.164400 ms after a second bounded cleanup attempt, even though the tail and peeled kernels both looked slightly better in isolation. In the latest NCU comparison against the accepted best 1181247 run, the dominant 128x128 hot-band kernel is the only kernel that actually got slower, moving from 32868864 ns to 32936736 ns while holding the same 196 registers and 22016 B shared-memory footprint. That makes the hot-band control path the clearest remaining primary family, and the PTX 128x128 branch is the best next move because it preserves the same overall tile geometry while swapping in a different export and inner-loop control path on the kernel that dominates total runtime.`
- expected bottleneck: `Dominant 128x128 hot-band control flow, especially cp.async wait cadence and export-scratch behavior inside the steady-state hot path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:107-142, src/kernels/bf16_gemm_v1.cu:930-1068, src/kernels/bf16_gemm_v1.cu:1955-2061, src/kernels/bf16_gemm_v1.cu:2090-2138`
- risk: `Moderate to high. This reopens the dominant kernel family on top of the accepted best base, so it can easily destabilize the main path if the PTX control flow does not produce a measurable hot-band win.`
- metrics to re-check: `end-to-end median runtime versus the 24.422464 ms 1181247 baseline, p10 and p90 runtime spread on the fixed perf run, 128x128 hot-band kernel gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active for the hot-band kernel, smsp__warp_issue_stalled_barrier_per_warp_active.pct for the hot-band kernel, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct for the hot-band kernel, launch__registers_per_thread and launch__shared_mem_per_block_allocated.sum for the hot-band kernel`

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
