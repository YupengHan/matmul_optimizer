# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Re-enable the 128x128x32 hot-band steady-state with the proven consume-before-overwrite fence`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_235645`
- round loop: `round 17/50`
- hypothesis: `Round 16 proved that the 128x128/128-thread hot-band family is structurally correct once the shared stage is kept live until all four warps finish consuming it. That means the best next move, aligned with the human-idea families around Async Copy, Pg2s, Ps2r, Data Reuse, and Stage, is not a new tile search but restoring the 2xK16-per-stage K32 steady-state on top of the now-proven stage contract. If the same consume-before-overwrite fence is applied to the K32 loop before reusing `a_shared[curr_stage]` and `b_shared[curr_stage]`, the branch should recover some of the 0.84 ms lost to the K16 control overhead while staying correct.`
- expected bottleneck: `Mainloop control and overlap efficiency in the corrected 128x128 family. The target is to raise tensor active back toward the earlier incorrect K32/K16 peaks without reopening the shared-stage race.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1469, src/kernels/bf16_gemm_v1.cu:1555, src/kernels/bf16_gemm_v1.cu:1565, src/kernels/bf16_gemm_v1.cu:1754`
- risk: `The K32 loop has two consumes per stage, so the fence placement must cover both MMA steps without unnecessarily serializing the stage. If the fence is too weak, correctness fails again; if it is too strong, the overlap gain disappears.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`

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
