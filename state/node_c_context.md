# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted-correct hot-band surface and apply a warp-local B XOR/interleaved consumer swizzle with zero extra shared footprint`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_232121`
- round loop: `round 13/50`
- hypothesis: `Round 12 showed that spending extra shared-memory budget on a deeper pipeline did not buy real hot-band speed: the main 256x128 kernel moved only from about 41.11 ms to 41.18 ms while barrier stalls jumped from about 6.59% to 20.24%, and correctness broke on top. That weakens the stage family for now. The user's remaining strongest untried constraint set is consumer-side B feed repair with three hard gates: no extra shared tile, no extra CTA barrier, no reduction in the steady-state pipeline. The current hot-band kernel still uses only a simple warp-group skew on B shared storage. A light XOR or interleaved remap in the logical B shared column mapping is the best next shot because it targets operand delivery directly while honoring those gates.`
- expected bottleneck: `Shared-memory bank behavior and warp-local B operand delivery in the hot-band PTX consumer path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:b_shared_col_from_logical, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:ptx_wmma_load_col_fragment_64x64, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `High. A broken remap silently corrupts results, and even a correct remap can worsen global-to-shared coalescing or register use enough to erase any bank benefit.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, runs/*/ncu_metrics.csv main 256x128 hot-band smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__shared_mem_per_block_allocated`

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
