# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Accepted PTX B-Reuse Branch And Clean Up Warp-Local Sequencing`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_013539`
- round loop: `round 40/100`
- hypothesis: `Round 39 proved that round 38's 25.974272 ms win was not a pure export-path effect: reverting the active PTX hot-band branch from the full consumer-side B-reuse helper back to the baseline accumulate helper, while keeping the padded export scratch, regressed to 26.733056 ms and restored the old stall mix of barrier 8.09, short_scoreboard 1.78, and mio 4.54. The next move should therefore start by restoring the accepted round-38 PTX branch exactly, then keep that full B-fragment reuse signal while cleaning up the warp-local consume sequence so it still suppresses mio_throttle but sheds some of the short_scoreboard and barrier cost that remained in the accepted branch. For this round the primary human-idea family is Register Reuse plus Ps2r plus Bank Conflict, with Async Copy, Pg2s, and Stage held fixed at the already-working double-buffer baseline.`
- expected bottleneck: `Warp-local consumer orchestration inside the active 128x128 K16 PTX hot loop, not CTA tiling or global-memory staging. The accepted branch drove mio_throttle down to 0.55% but paid 5.87% short_scoreboard and 11.13% barrier; the reverted branch restored the older 4.54% mio pattern. The highest-upside low-risk follow-up is to preserve the full reuse path and retime how B fragments are loaded and consumed within the warp.`
- code locations: `src/kernels/bf16_gemm_v1.cu:724 ptx_wmma_accumulate_col_tiles_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:745 ptx_wmma_accumulate_tile_set_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1895 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel`
- risk: `Medium. If the accepted full-reuse branch is not restored first, the experiment can collapse back into the already-losing baseline helper and give a false negative. Even with the correct base restored, changing warp-local sequencing can easily move pressure from mio into barrier or short_scoreboard without net runtime gain.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active`

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
