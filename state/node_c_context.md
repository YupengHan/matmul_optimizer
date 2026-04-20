# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Asymmetric PTX two-stage handoff retime without new barriers`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_170743`
- round loop: `round 3/20`
- hypothesis: `Round 2 gave clear negative evidence against treating helper/lifetime compaction as the main lever: shaving registers from 167 to 166 while slightly improving barrier, long scoreboard, and mio still regressed runtime badly to 34.70942307 ms. The next sustainable move should therefore stay on the accepted 64x384 PTX hot-band branch but change the actual overlap schedule rather than compiler-facing helper structure. Keep the current two-stage pipeline and unchanged 64x96 tail, then retime when A and B future-stage copies are launched and when the stage swap becomes visible inside advance_peeled_hot_stage_ptx(), so the one-block/SM kernel gets more useful compute between wait and next consume without adding CTA barriers or reopening producer-specialization.`
- expected bottleneck: `With occupancy still capped at 1 block/SM and barrier plus mio already low, the more actionable residual is long-scoreboard latency that is not being hidden well enough by the current steady-state handoff.`
- code locations: `src/kernels/bf16_gemm_v1.cu:194-208, src/kernels/bf16_gemm_v1.cu:503-529, src/kernels/bf16_gemm_v1.cu:821-854, src/kernels/bf16_gemm_v1.cu:895-948`
- risk: `Medium risk. The existing fixed-K retime is part of the winning base, so this must stay bounded: no extra stages, no extra barriers, and no producer/consumer split. If the retime only perturbs a working schedule, runtime can regress even if headline stalls look a bit better.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, median runtime`

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
