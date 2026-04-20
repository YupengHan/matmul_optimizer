# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Steady-state barrier / handoff retime`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_084003`
- round loop: `round 56/100`
- hypothesis: `The accepted PTX hot-band base is now limited most visibly by the barrier/handoff point in the steady-state loop. The right-left PTX consume order already proved the lane-local retime is live: runtime improved by 0.047009 ms at 24.849423 ms, and short scoreboard dropped from 3.02 to 1.52. Barrier rose from 6.42 to 7.43 and is now the clearest exposed limiter, so the next move is a very narrow retime around the active PTX hot-band loop handoff.`
- expected bottleneck: `Barrier latency at the active hot-band handoff, not stage count, macro tiling, grouped-row count, or warmup-order mechanics.`
- code locations: `src/kernels/bf16_gemm_v1.cu: hot-band steady-state loop handoff around the PTX consume order, src/kernels/bf16_gemm_v1.cu: barrier placement immediately before/after the active PTX hot-band consumer path, src/kernels/bf16_gemm_v1.cu: accepted PTX hot-band base in the async-copy / Pg2s / Stage path`
- risk: `A handoff retime can regress the already improved scoreboard balance if it widens the critical path or disturbs the accepted hot-band base.`
- metrics to re-check: `runtime_ms versus 24.849423 ms, barrier, short_scoreboard, warp stall balance at the hot-band handoff`

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
