# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted-correct hot-band surface and trade paired c_shared scratch for a 3-stage A/B pipeline`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_231606`
- round loop: `round 12/50`
- hypothesis: `Round 11 falsified the half-CTA Pg2s idea very clearly: the hot-band kernel slowed from about 41.11 ms to 46.14 ms while barrier stalls rose from about 6.59% to 23.43% and mio throttle rose from about 0.32% to 9.20%. That says the issue is not that too many threads participate in staging; it is that the current two-stage hot-band pipeline still does not hide feed latency well once orchestration changes. The next Pg2s move should therefore be deeper overlap, not fewer issuers. For the fixed 256x128 hot-band path specifically, the repo can likely afford a 3-stage A/B ring if the epilogue falls back from paired c_shared export scratch to a single-stage export helper. That directly matches the user's stage and epilogue-budget idea: spend a little more epilogue time to buy another A/B prefetch stage on the dominant hot loop.`
- expected bottleneck: `Tensor under-utilization from a too-shallow hot-band mainloop pipeline rather than pure DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile256x128, src/kernels/bf16_gemm_v1.cu:cp_async_wait_group_0, src/kernels/bf16_gemm_v1.cu:cp_async_wait_group_1, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `High. This changes both the hot-band mainloop schedule and the 64x64 export path, so correctness bugs can appear if the stage rotation or tail wait logic is wrong.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band launch__shared_mem_per_block_allocated`

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
