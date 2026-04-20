# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Make the 128x128 hot-band stage reuse safe before the next cp.async overwrite`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_235321`
- round loop: `round 16/50`
- hypothesis: `The 128x128/128-thread hot-band family is already the highest-ceiling branch we have seen, but the incorrect 28.36 ms run shows a logic race rather than a bad tile shape. The local debug reproduction indicates that adding a CTA fence immediately after each MMA consume and before reusing the same shared stage restores correctness on the failing case, which matches the human-idea families around Async Copy, Pg2s, Ps2r, and Stage more than any new tiling or bank-conflict change. Round 16 should therefore formalize that stage-reuse fix in the 128x128 K16 kernel and validate the performance cost with a full node_a measurement.`
- expected bottleneck: `Barrier / stage orchestration inside the hot-band mainloop. The goal is to trade a controlled barrier increase for removing the hidden producer-consumer race while preserving the much higher tensor utilization of the 128x128 branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1609, src/kernels/bf16_gemm_v1.cu:1662, src/kernels/bf16_gemm_v1.cu:1676, src/kernels/bf16_gemm_v1.cu:1692`
- risk: `The full CTA barrier may give back part of the 28.36 ms speedup. If tensor active collapses or barrier stall spikes into the CUTLASS gap, the fix is correct but too blunt and we will need a narrower producer-consumer fence.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
