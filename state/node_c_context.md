# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Narrow PTX Export Cleanup In The Row-Pair Helper`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_160556`
- round loop: `round 8/17`
- hypothesis: `Round 7/17 turned the minimal PTX export cleanup into a real new accepted base at 24.84582424 ms with correctness intact, lower DRAM, and lower long-scoreboard than the grouped-row retune. That is strong evidence that the export helper still has remaining low-risk headroom. The next best move is not to reopen the closed deeper flattening path, but to stay inside the same narrow family and trim the remaining repeated row-pair store/export plumbing in `ptx_wmma_store_tile_row_pair_64x64_ptx_microkernel` without changing scratch lifetime, traversal, or shared layout.`
- expected bottleneck: `Residual row-pair export helper setup and sync cadence inside the PTX store path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:925-949, src/kernels/bf16_gemm_v1.cu:1008-1065`
- risk: `Low to medium. The family just delivered a large win, but the earlier deeper export-flattening attempt already showed there is a boundary where the export cleanups stop helping.`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
