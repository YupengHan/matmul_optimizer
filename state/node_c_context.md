# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune the accepted B-first cp.async handoff inside the K16 hot band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_082833`
- round loop: `round 54/100`
- hypothesis: `The accepted round-52/53 base is still the right surface: grouped-row=8, K16, no B lookahead, single-scratch export, and B-first refill ordering. The latest run only regressed by 0.009152 ms, so the remaining gap looks like a very narrow steady-state handoff issue between cp.async issue, wait/commit timing, and the first PTX B-fragment consume order rather than a new memory-balance problem. Keep the accepted base intact and tighten only the B-first feed/issue handoff.`
- expected bottleneck: `Async-copy feed/issue retiming and stage handoff latency inside the active PTX hot-band microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1949-2005, src/kernels/bf16_gemm_v1.cu:1024-1049, src/kernels/bf16_gemm_v1.cu:720-769`
- risk: `Low to moderate. The upside is the best in this round, but it is easy to slide back into a disguised unroll-1 or lookahead-style rewrite if the handoff is changed too broadly.`
- metrics to re-check: `median runtime versus 24.895488 ms accepted base, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed`

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
