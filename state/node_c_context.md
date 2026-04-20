# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Start a CUTLASS-shaped hot-band branch: 128x128 CTA, 64x64 warp tiles, 128-thread launch, and K32 staged mainloop`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_232652`
- round loop: `round 14/50`
- hypothesis: `The plateau is now too persistent to justify more local tweaks. The current accepted-correct hot-band kernel runs with a 256-thread 256x128 CTA and reaches only about 38.13% tensor active, 17.00% DRAM throughput, and 6.83% barrier stalls. The recorded CUTLASS baseline on the same shape uses a 128-thread 128x128x32 multistage tensor-op kernel, reaches about 49.25% tensor active, 42.76% DRAM throughput, and only 0.39% barrier stalls, even with higher registers and more shared memory. That strongly suggests this GPU prefers a smaller CTA and a fatter K-stage that reduces coordination frequency while increasing useful bytes per stage. The next serious branch should therefore stop patching the 256x128 path and instead build a CUTLASS-shaped hot-band kernel specialized for this fixed benchmark: 128x128 CTA tiles, 64x64 warp tiles, 128 threads, and a K32 per-stage mainloop.`
- expected bottleneck: `Feed/orchestration inefficiency from the current 256-thread hot-band structure rather than a single bank-conflict or epilogue detail.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile256x128, src/kernels/bf16_gemm_v1.cu:PtxWmmaAccTileSet64x64, src/kernels/bf16_gemm_v1.cu:ptx_wmma_accumulate_tile_set_64x64, src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Very high. This is a new hot-band kernel family with tile-shape, launch-shape, and stage-shape changes all at once.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, runs/*/ncu_metrics.csv main hot-band dram__throughput.avg.pct_of_peak_sustained_elapsed, runs/*/ncu_metrics.csv main hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, runs/*/ncu_metrics.csv main hot-band launch__shared_mem_per_block_allocated, runs/*/ncu_metrics.csv main hot-band launch__registers_per_thread`

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
