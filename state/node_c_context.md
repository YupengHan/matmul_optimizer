# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Peel a fixed-shape steady-state hot kernel for 6464x7776x7232`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_095729`
- round loop: `round 4/5`
- hypothesis: `The evidence hierarchy now points away from more feed-path or live-set rewrites. The accepted base 16a98f7 is still best at 37.285807 ms. Round 1 two-level B staging and round 2 phased 64x384 micro-panels both regressed badly, and round 3 warp-specialized staging improved one symptom by cutting mio_throttle from 31.60% to 14.77% but still only reached 40.935423 ms because register pressure jumped to 168/thread, active warps collapsed to 16.59%, and barrier stall rose to 15.62%. That suggests the next move on the restored base should preserve the accepted 64x384 single-skew kernel shape and remove generic fixed-shape overhead instead: split the known 452-step K traversal into prologue, steady-state, and epilogue structure so the hot path no longer pays per-iteration branch and transition overhead.`
- expected bottleneck: `Generic steady-state loop/control overhead diluting tensor issue on the fixed-shape hot path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:421-450 (current generic K-loop with per-iteration next-stage branch, wait, and CTA barrier), src/kernels/bf16_gemm_v1.cu:517-550 (fixed benchmark launch path that can dispatch a more specialized hot kernel without changing the 64x384 + 64x96 decomposition), src/kernels/bf16_gemm_v1.cu:32-39 (tile-config shape parameters that the specialization should preserve)`
- risk: `This duplicates hot-path code and can make the kernel harder to maintain, and the benefit may be modest if memory/feed pressure still dominates after specialization.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
