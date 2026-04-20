# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim the active PTX export path and c_shared round-trip before touching feed again`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_011928`
- round loop: `round 38/100`
- hypothesis: `Primary family for round 38/100: export-path and shared-bank-overhead work on the active 128x128 K16 PTX hot-band branch. The branch had already recovered to 26.093568 ms, then two bounded consumer-side B-reuse iterations failed to convert their feed win into end-to-end speed: round 36 moved runtime to 26.128304 ms while collapsing mio_throttle from 4.45% to 0.48%, but short-scoreboard jumped from 1.67% to 5.89% and barrier from 8.05% to 10.95%; round 37 removed the next_b_frag lookahead and still regressed slightly again to 26.150880 ms with short-scoreboard 5.88%, barrier 10.90%, and mio_throttle still 0.48%. That is the stop condition for consumer-side B reuse as the current primary path. The next best move is to keep the active PTX hot loop stable and attack the untouched c_shared export chain directly: reduce paired-tile scratch traffic, trim shared-bank writes and LSU wavefronts in the BF16 export helpers, or narrow the per-warp round-trip so less synchronization sits after the MMA loop. This keeps the ranking centered on the active PTX branch and tests whether the feed-side improvement already exposed an epilogue-side shared bottleneck that now has more leverage toward the 20 ms goal.`
- expected bottleneck: `Shared-memory export overhead on the active PTX hot-band branch, especially c_shared bank writes, LSU wavefront pressure, and synchronization after the MMA loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:804-923, src/kernels/bf16_gemm_v1.cu:1811-1894, src/kernels/bf16_gemm_v1.cu:1944-1951`
- risk: `Medium. Export-only work is narrower than another feed rewrite, but it can shift cost into registers or awkward BF16 packing/stores and accidentally lower tensor issue if the scratch reduction is not disciplined.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, launch__shared_mem_per_block_allocated, launch__registers_per_thread`

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
