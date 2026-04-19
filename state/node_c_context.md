# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Async double-buffered K pipeline`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_210351`
- round loop: `round 1/5`
- hypothesis: `The kernel copies one K-slice, synchronizes, then computes, so the tensor cores spend too much time waiting on load completion. A pipelined prefetch path with double buffering should overlap global-memory latency with MMA work and cut the long-scoreboard stalls that dominate the current profile.`
- expected bottleneck: `Global-memory latency plus CTA-wide synchronization between K-slices, visible as long scoreboard stalls and barrier stalls in the steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Medium. The structure is still local to the current kernel, but async staging adds ordering complexity and can regress if the pipeline depth or buffer handoff is wrong.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime, TFLOP/s`

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

- no tracked dirty paths at prepare time
