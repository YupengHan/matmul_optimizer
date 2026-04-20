# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rewrite the active 128x128 K16 hot-band steady-state around Pg2s/Stage orchestration instead of dead grouped_rows tuning`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_003423`
- round loop: `round 33/50`
- hypothesis: `Primary human-idea family for round 33: `Async Copy` + `Pg2s` + `Stage` on the real default path. The measured hot kernel is `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel` launched at `src/kernels/bf16_gemm_v1.cu:1776`, not the grouped-order `128x128x32` kernel. Round 32 changed `kFixedHotBandGroupedRows`, but that knob is only consumed by the inactive `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel`, so the 27.130784 ms result is evidence that we should stop optimizing that dead L2-dispatch knob. On the actual active path, 16-byte wide global access and shared-memory reuse are already present, yet tensor-active is still only 48.24% while barrier stall is 8.04%, mio throttle is 4.31%, and DRAM/L2 are only 31.02% / 26.33%. The next best move is to keep the 128x128 CTA shape and 64x64 warp ownership, but restructure the K16 steady-state so stage recycle / commit / wait / sync are less intrusive: fewer full-CTA synchronization points, cleaner cp.async overlap, and no all-warps-copy behavior that dilutes tensor issue.`
- expected bottleneck: `Active hot-band feed/orchestration overhead in the K16 global-to-shared pipeline, dominated by synchronization and shared/L1/LSU delivery rather than external memory bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:869-895, src/kernels/bf16_gemm_v1.cu:1630-1726, src/kernels/bf16_gemm_v1.cu:1776-1783`
- risk: `Medium-high. The hot loop is already correctness-sensitive, and a deeper or re-phased pipeline can easily regress overlap, shared budget, or register pressure if the new schedule is not tightly bounded.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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
