# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Exact Fast PTX Default Hot-Band Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_113820`
- round loop: `round 77/100`
- hypothesis: `The non-PTX default hot-band dispatch promotion family is closed-negative for now. The round-76 auxiliary-256x128 default improved over the failed 64x384 path, but it is still far from the prior fast PTX regime: 31.86790371 ms vs about 24.696 ms. The cleanest recovery is to restore the exact fast PTX default hot-band path from the restored baseline, rather than keep iterating on promoted default dispatches. That means returning to the 128x128 PTX microkernel hot band with the peeled 384-row band and 96-column tail, which previously tracked the fast regime without the DRAM-heavy promotion behavior.`
- expected bottleneck: `The failed non-PTX default promotions are exposing barrier and memory inflation rather than a compute win, so the baseline PTX path should re-center the profile on the proven lower-overhead hot-band schedule.`
- code locations: `src/kernels/bf16_gemm_v1.cu:152-159, src/kernels/bf16_gemm_v1.cu:1908-2012, src/kernels/bf16_gemm_v1.cu:2064-2105`
- risk: `Medium. This is the most direct rollback to the prior fast regime, but it still has to be implemented cleanly so the wide-tile promotions do not stay latent in the default launch path.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__occupancy_limit_registers`

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
