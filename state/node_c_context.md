# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted unpeeled base, then tighten PTX export-scratch sync and lifetime while keeping linear export order`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_093804`
- round loop: `round 67/100`
- hypothesis: `Goal remains below 20 ms, and the best accepted custom result is still round 58 at 24.57088089 ms on commit 4e5579ec72e9b1f05820c895c0315235d66f30cd. Round 65 already closed export traversal reversal as negative, so the active export order should stay linear. Round 66 then restored linear export order but peeled the fixed-K steady state, and the runtime moved only trivially to 25.67372799 ms while barrier stall jumped from 5.27 to 6.65 and long scoreboard jumped from 7.59 to 14.82. That makes fixed-K peeling a closed-negative in its current one-sync K16 form and points back to the accepted base: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, and active-loop unroll 2. The best bounded next move is to restore that unpeeled base first, then shorten the PTX export scratch lifetime and trim the export-side sync/writeback closure without changing tile ownership or export traversal order. The current PTX export helper still performs shared export plus two warp syncs per 16x16 tile on a single padded scratch stage, so a smaller export-lifetime closure is a cleaner follow-up than reopening grouped_rows sweeps, consumer-order variants, or stage peeling.`
- expected bottleneck: `PTX export scratch live-range and warp-sync/writeback overhead on the accepted hot-band base after linear export order is restored.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile128x128PtxExportScratch, src/kernels/bf16_gemm_v1.cu:ptx_export_shared_tile_quads_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:ptx_wmma_store_tile_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel`
- risk: `Moderate. The change is correctness-sensitive because it touches the writeback/export path, but it is still a bounded one-node_c edit in the current PTX hot-band helper and does not reopen traversal reversal, grouped_rows retunes, or fixed-K peeling.`
- metrics to re-check: `median_runtime_ms versus 25.67372799 ms and the round-58 accepted 24.57088089 ms, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, l1tex__lsu_writeback_active.avg.pct_of_peak_sustained_elapsed, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, correctness on all three fixed BF16 cases`

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
