# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reuse one 16x16 epilogue scratch tile per warp with warp-synchronous pair stores`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260418_224925`
- round loop: `round 4/20`
- hypothesis: `Round 3 reduced the B-side bank pressure, but active warps still sit around 33% and the kernel still reserves 12.8 KB of shared memory per block, with most of the non-staging footprint coming from the three-tile-per-warp float `c_shared` epilogue buffer. Reusing a single 16x16 scratch tile per warp, then writing each MMA tile back immediately with warp-synchronous coordination, should lower the shared-memory footprint and the post-MMA shared round-trip without changing the main tensor-core loop.`
- expected bottleneck: `Shared-memory footprint and epilogue traffic are still constraining residency and keeping tensor utilization low after the B-tile skew fix. The current `c_shared` design stores all three output tiles per warp at once even though they are consumed strictly one tile at a time.`
- code locations: `src/kernels/bf16_gemm_v1.cu:29-33 (`kCSharedTileElemsPerWarp` and related shared-memory sizing constants), src/kernels/bf16_gemm_v1.cu:152 (`c_shared` declaration), src/kernels/bf16_gemm_v1.cu:216-233 (warp epilogue store and BF16 writeback loop)`
- risk: `Moderate. The epilogue becomes more serialized per warp, so a smaller scratch footprint must more than offset any extra loop overhead. Correctness also depends on preserving the existing WMMA store layout while rewriting the writeback loop.`
- metrics to re-check: `median runtime, TFLOP/s, launch__shared_mem_per_block_allocated, launch__occupancy_limit_shared_mem, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, correctness cases`

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
