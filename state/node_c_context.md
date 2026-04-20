# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: keep the outside-in signal, but recode it as a lower-pressure mirrored schedule`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_183726`
- round loop: `round 12/20`
- hypothesis: `Round 11 is the strongest new measured signal since the accepted base: a single change to the PTX accumulator traversal improved runtime from the demoted Stage branch back to 33.5528965 ms, only about 0.424 ms slower than the accepted 9bdc160 run. That means Idea 7 is real, not noise. But the current implementation also raised registers/thread from 167 to 172 and made barrier and mio stalls worse than the accepted base while only modestly lowering long scoreboard. The right round-12 move is therefore not a family pivot yet; it is one bounded follow-up inside Idea 7. Keep the outside-in reuse concept, but re-encode the 12-tile sweep in a compiler-friendlier mirrored schedule so it preserves the long-scoreboard improvement without paying the current barrier/mio/register tax.`
- expected bottleneck: `Warp-local issue-order pressure and codegen-induced register growth inside the 12-fragment PTX sweep, showing up as higher barrier and mio stalls even though long scoreboard improved.`
- code locations: `src/kernels/bf16_gemm_v1.cu:388-419, src/kernels/bf16_gemm_v1.cu:823-824, src/kernels/bf16_gemm_v1.cu:928-965`
- risk: `This is a narrow optimization lane. If the current outside-in order already captured essentially all of the reuse benefit, the follow-up may only reshuffle tiny effects or regress back toward the accepted base. It also risks turning into another codegen experiment if the schedule is rewritten too abstractly.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread`

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
