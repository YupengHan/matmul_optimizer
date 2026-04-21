# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_175514`
- round loop: `round 2/50`
- hypothesis: `Round 2/50 starts from a clear negative result: the latest measured K32 hot-band branch at run `20260420_175429_bf16_gemm_v1_134ec64` regressed end-to-end runtime from 25.47660828 ms to 30.29759979 ms. The dominant hot-band kernel itself got markedly worse versus the restored accepted PTX branch: kernel time rose from 32.97 ms to 39.57 ms, registers climbed from 200 to 212, shared memory rose from 22.016 KiB to 43.008 KiB, tensor activity fell from 47.72% to 40.05%, and barrier stall jumped from 5.52% to 10.04%. That closes the K32 family for now. Because the implementation surface has already been restored to the accepted `da1a5bb` PTX microkernel, the best next move is not another structural hot-band rewrite but the strongest already-measured PTX-adjacent fallback on that surface: restore the 4-row grouped traversal window, which earlier beat the current restored base at 25.40644836 ms while staying inside the same hot-band kernel family.`
- expected bottleneck: `CTA grouping and orchestration overhead around the accepted PTX hot-band grouped-row mapping, not the hot-band inner K-stage itself.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:1967-1979, src/kernels/bf16_gemm_v1.cu:2097-2104`
- risk: `Medium. This is a narrow and already measured control on the restored surface, but it still changes launch-order locality and can regress if the current hybrid-prefetch base interacts differently with the older 4-row window.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
