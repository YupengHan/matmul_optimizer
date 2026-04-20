# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Hot-Band Accumulator And Fragment Live Ranges`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_022105`
- round loop: `round 45/100`
- hypothesis: `Round 44 already recovered from 30.126080 ms to 26.955776 ms by removing K32 and switching to single-scratch sequential export, but versus round 42 the hot-band signals only moved slightly: tensor active 47.86 -> 48.05, mio throttle 0.56 -> 0.34, barrier 11.18 -> 11.21, and long scoreboard 1.29 -> 1.33. That says export lifetime trimming helped a little, but the remaining ceiling is inside the active PTX 128x128 hot-band compute path itself. The main kernel still runs at 188 registers/thread with occupancy limited to 2 blocks/SM and only 16.58% active warps, so shrinking accumulator / fragment live ranges inside the PTX microkernel should raise resident warps and let the tensor pipe cross the current 26 ms band instead of only restoring prior regressions.`
- expected bottleneck: `Occupancy and tensor-core under-utilization in the active PTX hot-band path, driven by register pressure rather than global-memory latency.`
- code locations: `src/kernels/bf16_gemm_v1.cu:709, src/kernels/bf16_gemm_v1.cu:725, src/kernels/bf16_gemm_v1.cu:746, src/kernels/bf16_gemm_v1.cu:1888, src/kernels/bf16_gemm_v1.cu:1940, src/kernels/bf16_gemm_v1.cu:1985`
- risk: `Reducing live ranges can easily trade one bottleneck for another: less unrolling or fewer simultaneously resident fragments may cut instruction-level parallelism, lower tensor issue efficiency, or force extra shared-memory round trips. The risk is acceptable because the current evidence already says the export path is no longer the main limiter.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, launch__occupancy_limit_registers, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`

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

- `src/kernels/bf16_gemm_v1.cu`
