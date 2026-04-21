# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Activate 128x128x32 Two-K Hot-Band Staging`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_193848`
- round loop: `round 14/50`
- hypothesis: `Round 14 has no extra human idea family in `state/human_review.md` beyond the approval gate, so the first diagnosis step is to accept the restored accepted-dispatch baseline and continue from it rather than reverting again. The latest run recovered the correct `128x128 + residual 64x384 + 64x96 tail` path and jumped back to `25.504256 ms`, but it still trails the accepted `1181247` best at `24.422464 ms`. The dominant `128x128` hot-band kernel is still the only place with enough weight to explain that remaining gap, and its current metrics are slightly worse than the accepted best on the same branch (`47.69%` tensor active vs `48.24%`, `7.77%` long scoreboard vs `7.49%`, `5.65%` barrier vs `5.58%`). The dormant `128x128x32` kernel preserves the accepted grouped-row `128x128` geometry while changing only stage cadence to consume two K16 slices per handoff, making it the best next upside/risk tradeoff on the recovered branch.`
- expected bottleneck: `Hot-band stage cadence and feed overlap in the accepted `128x128` branch, not dispatch selection or the already-rejected full-band `64x384` family.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1077-1098, src/kernels/bf16_gemm_v1.cu:1687-1840, src/kernels/bf16_gemm_v1.cu:2071-2138`
- risk: `Moderate. The branch already exists and keeps the accepted geometry, but it is dormant, so shared-memory footprint, occupancy, or correctness can regress before any stage-cadence gain appears.`
- metrics to re-check: `end-to-end median runtime versus the `24.422464 ms` accepted best and the current `25.504256 ms` run, hot-band `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`, hot-band `smsp__warp_issue_stalled_barrier_per_warp_active.pct`, hot-band `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`, hot-band `launch__shared_mem_per_block_allocated` and `launch__occupancy_limit_registers``

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
