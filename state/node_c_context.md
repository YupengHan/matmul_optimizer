# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 9 Ps2r: slice-local two-fragment ping-pong on the full-width PTX sweep`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_174046`
- round loop: `round 6/20`
- hypothesis: `Mapping: this direction is a direct refinement of human idea 9, Ps2r shared-to-register double buffering. Round 5 gave positive but insufficient evidence for this family: runtime improved and long-scoreboard dropped from 6.22 to 5.98, so Ps2r is real signal, not noise. What it did not fix was tensor activity and barrier pressure. The next practical move is therefore not to abandon Ps2r, but to make it more structured: keep the accepted 64x384 hot-band PTX kernel and unchanged 64x96 tail, then replace the current flat 12-tile walk with explicit small slices that ping-pong two B fragments in registers while the slice's mma chain executes. The aim is to preserve the round-5 scoreboard gain while tightening the live/use window enough to recover tensor issue without reopening CTA-level retiming.`
- expected bottleneck: `Warp-local shared-to-register latency is now a proven residual limiter, but the current Ps2r form is not organized tightly enough to convert that stall reduction into better tensor issue.`
- code locations: `src/kernels/bf16_gemm_v1.cu:273-299, src/kernels/bf16_gemm_v1.cu:388-402, src/kernels/bf16_gemm_v1.cu:801-818, src/kernels/bf16_gemm_v1.cu:910-948`
- risk: `Medium risk. The slice-local ping-pong can raise registers or turn into a cosmetic reorder if the fragment scope is not actually tightened. It is still the best next step because it builds directly on the only recent direction that improved the targeted stall without reopening a rejected family.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread, launch__occupancy_limit_registers, median runtime`

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
