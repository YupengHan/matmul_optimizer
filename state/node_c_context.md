# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea Ps2r: one-fragment shared-to-register lookahead on the restored streaming-B branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_215602`
- round loop: `round 2/30`
- hypothesis: `The restored round-8 branch already cleaned up the B consumer issue order enough to collapse `mio_throttle` without increasing registers or shared memory, but tensor active is still only about 38.56% and occupancy remains register-limited at one block. The next direct feed-side step is to overlap the next B fragment load from shared to registers with the current MMA issue chain inside the 64x64 hot-band micro-tile. Because the branch now already streams one B fragment at a time in mirrored order, a one-step Ps2r lookahead is a cleaner and more targeted experiment than further shared permutations.`
- expected bottleneck: `Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the streaming consumer cleanup.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_tiles_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Moderate to high. This branch is already near the register wall, so the lookahead has to be very small and local. If registers climb meaningfully, the win is probably lost immediately.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, launch__occupancy_limit_registers, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed`

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
