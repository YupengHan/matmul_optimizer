# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the active PTX B-fragment reuse, but rewrite warp-local sequencing to shrink the new short-scoreboard and barrier cost`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_011150`
- round loop: `round 37/100`
- hypothesis: `Primary family for round 37/100: Register Reuse + Ps2r + Bank Conflict on the active 128x128 K16 PTX hot-band branch, but now as sequencing cleanup instead of a more aggressive reuse expansion. Round 36 proved the consumer-side B idea has real signal: runtime only regressed from 26.093568 ms to 26.128304 ms while mio_throttle collapsed from 4.45% to 0.48% and long-scoreboard stayed flat at 1.20%. The failure mode is that the current helper loads four A fragments up front, holds one mirrored-column B fragment across both 32-row pairs, and recursively preloads the next B fragment; that likely over-extends the warp-local live set and exposes a tighter dependency chain, which shows up as short-scoreboard jumping from 1.67% to 5.89% and barrier from 8.05% to 10.95%. The next move is to preserve the same B-fragment reuse target, but rewrite the consume order so fewer fragments are live at once and the next Ps2r load lands closer to use: for example, a late-load row-pair-2/3 phase or an explicit Right-Left-Right-Left mirrored sweep that keeps only one A row pair and one lookahead B fragment live at a time. Do not add CTA repack, deeper stages, or a new macro tile; keep the current producer path and two-stage K16 pipeline intact.`
- expected bottleneck: `Warp-local consumer sequencing and fragment live-set pressure in the active PTX hot-band branch, where the current B-reuse schedule traded mio_throttle for short-scoreboard, extra synchronization exposure, and higher DRAM/L2 traffic.`
- code locations: `src/kernels/bf16_gemm_v1.cu:687-747, src/kernels/bf16_gemm_v1.cu:1858-1896, src/kernels/bf16_gemm_v1.cu:1952-1959`
- risk: `Medium-high. This keeps the promising B-reuse idea alive, but the active PTX branch is correctness- and register-sensitive; a bad consume order can easily give back the mio win, inflate registers, or break fragment ownership.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, lts__throughput.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread`

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
