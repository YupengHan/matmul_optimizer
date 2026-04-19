# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Full-width PTX fragment-issue scheduling with tighter live ranges`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_142321`
- round loop: `round 1/20`
- hypothesis: `The restored accepted PTX base is still winning because orchestration and paired export already worked, but the remaining shape is clear: barrier and mio are low, occupancy is still 1, and long scoreboard is now the more visible residual stall. The best long-run next step is a full-width 64x384 PTX dataflow follow-through that does not reopen the regressed half-panel compute split and does not panelize B-load reorder. Instead, flatten the hot-band fragment issue order so each B fragment is loaded and consumed in a tighter scope inside the existing 12-tile kernel, reducing compiler-visible live ranges without changing the outer tile or the 64x96 tail.`
- expected bottleneck: `Residual long-scoreboard latency and register-limited live state inside the current full-width PTX helper surface are now more limiting than synchronization overhead.`
- code locations: `src/kernels/bf16_gemm_v1.cu:261-299, src/kernels/bf16_gemm_v1.cu:388-402, src/kernels/bf16_gemm_v1.cu:801-818, src/kernels/bf16_gemm_v1.cu:915-948`
- risk: `This is still PTX-local but not trivial: changing the full-width issue order can increase instruction count or accidentally drift toward the already-losing half-panel explicit mma.sync path. The payoff may also be modest if the compiler already keeps the fragment lifetimes tighter than expected.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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
