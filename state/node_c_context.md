# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Accepted PTX Branch And Tighten Export Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_015436`
- round loop: `round 42/100`
- hypothesis: `Round 41 is a clear negative result for explicit producer partitioning on the active 128x128 K16 PTX branch: runtime regressed from the accepted round-38 branch at 25.974272 ms (commit e26d834, run 20260420_012953_bf16_gemm_v1_e26d834) to 27.261951 ms, while mio stayed very low at 0.48% and barrier inflated to 14.61%. That makes Async Copy and Pg2s producer partitioning a reject for this round, not a reason to abandon the accepted PTX branch. The best next move is to restore that accepted full-B-reuse branch first and keep pushing the still-live Bank Conflict family on the export side: refine the padded c_shared scratch, pair packing, or warp-local export sequencing so the branch keeps its good feed behavior but spends fewer cycles in export-side shared traffic and sync.`
- expected bottleneck: `Shared-memory export overhead and warp-local synchronization in the PTX c_shared round-trip, now showing up mainly as barrier and short-scoreboard stalls rather than mio or DRAM starvation.`
- code locations: `src/kernels/bf16_gemm_v1.cu:134 FixedHotBandTile128x128PtxExportScratch, src/kernels/bf16_gemm_v1.cu:882 ptx_export_shared_tile_quads_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:964 ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1002 ptx_wmma_store_tile_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1945 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel`
- risk: `Medium. The accepted branch is already close to the current best, so export edits must preserve correctness, shared-memory budget, and the existing full-B-reuse feed path. Any extra sync or larger scratch can erase the gain immediately.`
- metrics to re-check: `median_runtime_ms, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed`

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
