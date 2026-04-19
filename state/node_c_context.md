# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Deepen single-skew cp.async overlap in the fixed peeled 64x384 hot kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_101657`
- round loop: `round 1/5`
- hypothesis: `The current best result already confirms the right foundation: peeled fixed-shape hot loop plus trimmed export path. Relative to the older accepted base, tensor active is up at 34.53% and barrier stall is down at 6.39%, so the remaining gap is no longer control-heavy. What still stands out is 14.23% short-scoreboard, 30.42% mio_throttle, about 41.77% DRAM throughput, and about 82.75% LSU request pressure on the hot peeled kernel. The best next move is therefore a bounded overlap retune inside the existing single-skew peeled loop: keep the 64x384 tile and current layout, but rework commit/wait timing, prefill placement, or stage usage so more of the peeled loop runs against in-flight copies instead of exposed latency.`
- expected bottleneck: `Copy-latency exposure and in-loop feed overlap in the peeled 64x384 hot kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:41-58 (current shared-memory budget and stage-count constraints), src/kernels/bf16_gemm_v1.cu:189-199 (cp.async commit and wait helpers), src/kernels/bf16_gemm_v1.cu:567-605 (peeled hot-loop prefill, next-stage issue, and wait/barrier sequence)`
- risk: `The current kernel is already a new best, so overlap retuning can easily move the pipeline the wrong way and give back the peeled-hot-path win without a large enough upside.`
- metrics to re-check: `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
