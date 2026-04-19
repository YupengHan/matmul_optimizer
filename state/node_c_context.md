# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea: vectorize transfers and thread-coarsen the load/store path`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260419_003032`
- round loop: `round 14/20`
- hypothesis: `Round 13 made it clear that the kernel is highly sensitive to MIO and ld/st pressure. Starting from the restored accepted base, push a human-in-loop optimization that reduces instruction count on the load/store side: keep each memory instruction moving more data by vectorizing contiguous BF16 traffic and thread-coarsening the copy/store work so fewer instructions cover the same bytes. The likely first payoff is in the epilogue and any scalarized staging loops that still serialize BF16 movement too finely.`
- expected bottleneck: `MIO throttle and LSU pressure from too many narrow load/store instructions in the hot path and epilogue.`
- code locations: `src/kernels/bf16_gemm_v1.cu: stage_a_shared_tile_async and stage_b_shared_tile_async copy loops, src/kernels/bf16_gemm_v1.cu: the epilogue block after the K loop (`wmma::store_matrix_sync`, BF16 conversion, and final `c[...]` stores), src/kernels/bf16_gemm_v1.cu: any helper additions needed for vectorized BF16 packing / wider stores and per-thread coarsened store ownership`
- risk: `Medium-high. Vectorization and thread coarsening can increase register pressure, create alignment bugs, or make per-thread work imbalance worse if applied too aggressively.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, median runtime`

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
