# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Hot-Band Register And Export Lifetime`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_021122`
- round loop: `round 44/100`
- hypothesis: `Round 43's K32 staged PTX hot-band experiment is now a measured negative result: barrier stall fell from 11.18% to 4.80%, but runtime regressed from 27.003904 ms to 30.126080 ms while tensor active dropped from 47.86% to 43.84%, `mio_throttle` rose from 0.56% to 2.37%, and `long_scoreboard` rose from 1.29% to 4.35%. The active 128x128 PTX microkernel also grew from 188 to 196 registers per thread and from 28.160 KB to 45.056 KB shared memory per block, so the next move should recover Tensor Core issue rate by shortening live state in the PTX export and accumulator path rather than deepening the async pipeline again.`
- expected bottleneck: `Register pressure and export-side live-range bloat in the active PTX hot-band branch are suppressing active warps and tensor issue efficiency after the failed K32 stage expansion.`
- code locations: `src/kernels/bf16_gemm_v1.cu:134-142 FixedHotBandTile128x128PtxExportScratch, src/kernels/bf16_gemm_v1.cu:967-1014 ptx_wmma_store_tile_row_pairs_64x64_ptx_microkernel / ptx_wmma_store_tile_pairs_64x64_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1898-2033 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel`
- risk: `Medium. This stays inside the active hot-band PTX branch and targets the new regression signature directly, but export/accumulator lifetime changes can easily trade register savings for extra instructions or correctness bugs.`
- metrics to re-check: `median runtime, gpu__time_duration.sum for bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, launch__shared_mem_per_block_allocated, launch__occupancy_limit_registers`

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
