# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Hot-band L2 / grouped-row launch-order refinement`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_084408`
- round loop: `round 57/100`
- hypothesis: `The latest measured run 20260420_084312_bf16_gemm_v1_57d08c3 at 24.713584 ms already validated the steady-state handoff retime, with runtime improving by 0.135839 ms and barrier pressure falling from 7.43 to 5.45. Long scoreboard rose to 7.29 while LTS stayed around 30.75 and DRAM stayed low at 9.74, so the cheapest remaining locality lever is to refine kFixedHotBandPtxGroupedRows / hot-band launch order to increase reuse of the same B tile before advancing to the next x tile.`
- expected bottleneck: `Improved L2 locality and reduced B-tile churn should trim long scoreboard pressure without reopening the already-accepted one-sync handoff base.`
- code locations: `src/kernels/bf16_gemm_v1.cu: kFixedHotBandPtxGroupedRows, src/kernels/bf16_gemm_v1.cu: bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu: launch_bf16_gemm_v1`
- risk: `If the grouping becomes too coarse, the launch order can reduce locality for one axis while helping the other, and any win may be small because DRAM is already low.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
