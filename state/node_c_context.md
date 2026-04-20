# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the exact accepted round-58 implementation surface first, then re-measure from that true base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_104405`
- round loop: `round 69/100`
- hypothesis: `Goal remains below 20 ms, and the accepted best custom result is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Round 68 regressed to 25.85795212 ms, so the grouped_rows=8 snake launch-order mapping is closed-negative. More importantly, the current source no longer looks like a clean accepted-base anchor plus only the latest narrow experiment. The supervisor already diffed src/kernels/bf16_gemm_v1.cu against accepted commit 4e5579e and found surviving deltas beyond the snake mapping: the removed second syncwarp in ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel, the B-before-A stage order in advance_peeled_hot_stage_ptx, the 256x128 hot-band unroll changed from 1 to 2, the extra RowPairBase template parameter in ptx_wmma_load_col_fragment_64x64_ptx_microkernel, and the current snake mapping itself. That is auditable evidence that the loop may be exploring from a drifted surface rather than the true accepted base. The highest-value next move is therefore to restore the exact accepted implementation surface first, including undoing the snake mapping and any other non-accepted drift that can touch active paths, and then re-measure before spending another round on micro-optimizations.`
- expected bottleneck: `Baseline drift and false-anchor risk rather than a single hot-path micro-bottleneck; the loop needs the true accepted surface back before further diagnosis is trustworthy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:advance_peeled_hot_stage_ptx, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_col_fragment_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel`
- risk: `Moderate. This touches several places in one file, but it is still a bounded restore-to-known-surface change rather than another fresh speculative rewrite, and it directly resolves the current ambiguity about what base the loop is actually standing on.`
- metrics to re-check: `median_runtime_ms against 25.85795212 ms and the accepted 24.57088089 ms result, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, correctness on all three fixed BF16 cases`

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
