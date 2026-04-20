# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 5/7 Bank conflict + internal-tile order: keep the correct 256x128 hot kernel, but change the 64x64 warp-consumer order to Right/Left/Right/Left`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_210642`
- round loop: `round 5/10`
- hypothesis: `After the round-4 reset, the loop is back on a correct branch whose true hotspot is again the fixed hot-band 256x128 kernel at about 40.91 us with 167 registers/thread, occupancy_limit_registers = 1, tensor active around 38.0, and active warps around 16.6. That means the correct branch is back to the original feed/orchestration wall: not DRAM-bound, not L2-bound, and still under-occupying because the full 64x64 warp tile is fed in a flat left-to-right order. The user's human ideas map cleanly here: keep the accepted 256x128 / 64x64 tiling, keep wide cp.async coalescing and shared reuse unchanged, but retune the internal warp issue/load order as Right Left Right Left. Concretely, make the hot-kernel B-fragment consumption and MMA order alternate outer and inner tile columns instead of sweeping 0-1-2-3 monotonically. This is a warp-local consumer transform on the correct branch, not another CTA repack or macro-tile experiment.`
- expected bottleneck: `Warp-local B-consumer delivery and internal fragment issue order on the true hot-band kernel. A win should show up as slightly higher tensor active and lower hot-band time without changing shared memory footprint or stage depth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_mma_row_pair_col_pair_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_col_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_row_pairs_64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `The ceiling is moderate. Registers may stay near 167/thread, so this will not solve the whole occupancy wall by itself. The guardrail is that the branch stays correct and does not add new shared traffic or barriers.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__registers_per_thread`

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
