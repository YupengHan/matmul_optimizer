# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep The Accepted PTX Base And Close Within-Group Launch-Order Locality`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_094627`
- round loop: `round 68/100`
- hypothesis: `Round 67 showed that export-path micro-closure is no longer the primary lever: removing the second export-side syncwarp from the PTX hot-band helper left runtime flat at 25.67680073 ms, while long_scoreboard collapsed from 14.82 to 4.20 and barrier only eased from 6.65 to 6.51. That means the accepted active base should stay exactly where it is now: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, active-loop unroll 2, and the trimmed export helper with only the first syncwarp retained. The next highest-ceiling still-open family is therefore L2 cache swizzle or launch-order locality inside that fixed grouped_rows=8 base: change only the within-group physical_pid to logical_block mapping or block issue order so nearby CTAs reuse hot-band B and scratch working sets more effectively without reopening grouped_rows retunes or any consumer-order sweep.`
- expected bottleneck: `CTA issue-order locality and L2 reuse inside the active PTX hot-band mapping, not export scratch synchronization. DRAM is already low while L2 remains materially active, so the remaining upside is more likely in how grouped_rows=8 CTAs are sequenced than in another export-side micro-trim.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156 kFixedHotBandPtxGroupedRows, src/kernels/bf16_gemm_v1.cu:1928 hot-band tile geometry in bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1932 physical_pid to logical_block mapping inside the active PTX kernel, src/kernels/bf16_gemm_v1.cu:2019 launch_bf16_gemm_v1 fixed-shape PTX hot-band dispatch`
- risk: `Medium. It is easy to accidentally smuggle grouped_rows retunes back in under a locality label, or to change block order without creating any real cache benefit. This direction must keep grouped_rows fixed at 8 and preserve the accepted consume, refill, and export order exactly.`
- metrics to re-check: `median runtime, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active`

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
