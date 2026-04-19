# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reduce stage-recycle barriers in the peeled 64x384 hot loop`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_102638`
- round loop: `round 2/5`
- hypothesis: `The current best base confirms the right family: peeled fixed-shape hot kernel plus trimmed export, with deeper single-skew overlap improving again to 35.677088 ms. The residual tradeoff is now clear in the hot kernel profile: short scoreboard collapsed to 0.39% and DRAM dropped to 27.32%, but barrier stall climbed to 15.46% while tensor active slipped slightly versus the previous base. That makes the best next move a bounded refinement of the peeled overlap schedule itself: keep the same single-skew feed path and 64x384 tile, but reduce the number or scope of full-CTA stage-recycle barriers so the overlap gain survives without paying as much synchronization cost.`
- expected bottleneck: `CTA-wide synchronization and stage handoff overhead inside the peeled 64x384 steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:189-199 (cp.async commit and wait helpers), src/kernels/bf16_gemm_v1.cu:567-607 (peeled hot-loop prefill, future-tile refill, wait_group_1, and full-CTA barriers), src/kernels/bf16_gemm_v1.cu:538-542 (two-stage shared buffers whose reuse currently forces the recycle synchronization)`
- risk: `The current kernel is already the best custom result, so reducing barriers can easily re-expose short-scoreboard or create stage-reuse races if the synchronization boundary moves too far.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
