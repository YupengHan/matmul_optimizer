# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Skew the B shared tile with a bank-conflict-avoidance swizzle`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260418_222704`
- round loop: `round 3/20`
- hypothesis: `The accepted 16x48 BF16 B tile is still loaded through `wmma::load_matrix_sync` with a 48-element shared stride, so each row advances by 96 bytes and repeatedly aliases the same shared-memory banks during the three adjacent matrix_b fragment loads. Adding a per-row skew to the staged B tile, while preserving 16-byte async-copy granularity, should cut the remaining `mio_throttle` and short-scoreboard pressure without undoing the 3xN reuse win from round 2.`
- expected bottleneck: `Residual bank conflicts and port contention on the shared-memory-to-WMMA B-fragment feed path, which still show up as `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 25.61` and `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct = 11.28` even after the tile-retune improvement.`
- code locations: `src/kernels/bf16_gemm_v1.cu:22-36 (`kTensorBlockN`, `kBSharedTileElems`, async-copy sizing constants), src/kernels/bf16_gemm_v1.cu:82-93 (`stage_b_shared_tile_async` shared-store layout), src/kernels/bf16_gemm_v1.cu:147 (`b_shared` declaration), src/kernels/bf16_gemm_v1.cu:196-201 (`wmma::load_matrix_sync` B-fragment loads and leading dimension)`
- risk: `Moderate. The skew must preserve both `cp.async` alignment and the logical row-major matrix view expected by `wmma::load_matrix_sync`; a bad stride choice can silently corrupt results or increase shared-memory footprint enough to hurt occupancy.`
- metrics to re-check: `median runtime, TFLOP/s, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__shared_mem_per_block_allocated, correctness cases`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
