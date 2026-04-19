# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the low-footprint wide B slab and keep any new swizzle occupancy-neutral`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_231124`
- round loop: `round 7/20`
- hypothesis: `This regression tracks the B shared-memory relayout more than any improvement in the steady-state feed path. Compared with the accepted base run, the 16x16 subtile layout raised static shared memory from 12.800 KB/block to 15.360 KB/block, dropped `launch__occupancy_limit_shared_mem` from 7 to 6 CTAs per SM, and reduced `sm__warps_active.avg.pct_of_peak_sustained_active` from 58.03% to 49.78%. At the same time, `l1tex__data_bank_reads` rose from 13.55% to 15.16% and `l1tex__data_pipe_lsu_wavefronts` rose from 66.09% to 72.79%, so the subtile scheme paid both a residency cost and a shared-load cost. The next implementation round should restore the accepted wide 16x96 B slab first, then only try B-side swizzles or padding that keep the accepted shared-memory footprint intact.`
- expected bottleneck: `Shared-memory footprint and B-fragment load efficiency are cutting block residency and leaving the tensor loop underfed.`
- code locations: `src/kernels/bf16_gemm_v1.cu:36-49 (B shared-layout constants and per-tile footprint math), src/kernels/bf16_gemm_v1.cu:98-111 (`stage_b_shared_tile_async` packing into shared memory), src/kernels/bf16_gemm_v1.cu:164-166 and 216-220 (`b_shared` allocation and B fragment load addresses)`
- risk: `Low to moderate. Restoring the accepted base is known-good, but any follow-on swizzle still has to preserve 16-byte `cp.async` alignment and WMMA row-major fragment semantics without reintroducing the same shared-memory footprint increase.`
- metrics to re-check: `median_runtime_ms, launch__shared_mem_per_block_allocated, launch__occupancy_limit_shared_mem, sm__warps_active.avg.pct_of_peak_sustained_active, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness_passed`

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

- no tracked dirty paths at prepare time
