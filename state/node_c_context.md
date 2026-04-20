# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 1 Tiling: pivot to a new 256x128 CTA / 64x64 warp hot-band branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_184408`
- round loop: `round 13/20`
- hypothesis: `Idea 7 delivered two real wins, but round 12 strongly suggests that family is now near its local limit. The second follow-up improved runtime by only 0.1254406 ms, leaving the kernel still 0.2990093 ms slower than the accepted base, while tensor, barrier, long-scoreboard, mio, and active-warps were essentially unchanged. That is exactly the signature of a family approaching stop_condition: small runtime nibble, no new machine-state shift. Because the user target remains 20 ms, the next best move is a higher-ceiling pivot, not another narrow traversal tweak. Human idea 1 is the cleanest such pivot: open a genuinely different hot-band hierarchy at 256x128 CTA and 64x64 warp tiling, keeping the fixed shape and 64x96 tail specialization but moving out of the 64-row CTA family whose measured local sweet spot is already well explored.`
- expected bottleneck: `Current 64x384 hot-band hierarchy is near a family-level ceiling; the remaining gap is dominated by tile hierarchy rather than another small warp-local scheduling tweak.`
- code locations: `src/kernels/bf16_gemm_v1.cu:26-77, src/kernels/bf16_gemm_v1.cu:561-643, src/kernels/bf16_gemm_v1.cu:875-980`
- risk: `High implementation risk and likely multi-round exploration cost. This is a structural branch, so the first round may only establish correctness and feasibility rather than immediate performance. It can easily regress if the new hierarchy explodes register pressure or fragments the fixed-shape hot path.`
- metrics to re-check: `median runtime, correctness, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__registers_per_thread, launch__occupancy_limit_registers`

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
