# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rebalance PTX B Fragment Reuse Against Ps2r Feed Pressure`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_074354`
- round loop: `round 48/100`
- hypothesis: `Round 47's grouped-row increase from 4 to 8 already pushed the hot PTX band to a new best custom runtime of 25.529328 ms and cut DRAM throughput from 12.90% to 10.37% while lifting L2 throughput from 29.45% to 30.02%. That confirms block-order locality is still helping, but the remaining bottleneck has not moved to global memory. The active PTX microkernel still reloads the mirrored-column B fragment for every row-pair, which matches the still-elevated mio_throttle at 4.77% and suggests the next material win is to reduce shared-to-register feed pressure instead of chasing another small locality-only gain. Reintroducing a controlled B-fragment lookahead or a two-fragment rolling window in the PTX 128x128 path should cut Ps2r traffic without giving back the locality win from grouped-row=8.`
- expected bottleneck: `Ps2r/shared-feed pressure in the PTX hot-band microkernel, showing up as elevated mio_throttle and underfed tensor issue despite lower DRAM demand.`
- code locations: `src/kernels/bf16_gemm_v1.cu:641, src/kernels/bf16_gemm_v1.cu:721, src/kernels/bf16_gemm_v1.cu:743, src/kernels/bf16_gemm_v1.cu:1018, src/kernels/bf16_gemm_v1.cu:1979`
- risk: `Keeping more B fragments live can raise register pressure above the current 94 registers/thread and erase the gain by reducing latency hiding or perturbing the mirrored-column ownership. A careless rewrite can also reintroduce the longer export/live-range problem that the current PTX path was designed to trim.`
- metrics to re-check: `median runtime and TFLOP/s against the 25.529328 ms best custom baseline, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active`

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
