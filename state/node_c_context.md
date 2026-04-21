# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Specialize The Peeled 64x384 Residual Band On The New Best Sibling Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_185444`
- round loop: `round 9/50`
- hypothesis: `The human-review queue does not add any new manual idea bullets for round 9, so the primary accepted family is the smallest evidence-backed cleanup on top of the new best sibling base rather than a fresh kernel-family pivot. In the latest run, the main 128x128 sibling hot-band path is already the accepted best at 24.422464 ms, while the residual 64-row peeled 64x384 kernel still costs about 0.907 ms, allocates 46592 B of shared memory, uses 172 registers per thread, and spends 18.62% of warp cycles in barrier stalls. Giving that residual path a tighter epilogue and export scratch, instead of leaving it on the older two-stage 64x384 cleanup path, is the best next move because it targets the clearest remaining bounded outlier without perturbing the dominant hot-band kernel that just became the new best run.`
- expected bottleneck: `Peeled 64x384 residual-kernel epilogue shared-export traffic and barrier serialization after the hot-band handoff.`
- code locations: `src/kernels/bf16_gemm_v1.cu:24-63, src/kernels/bf16_gemm_v1.cu:1150-1164, src/kernels/bf16_gemm_v1.cu:1472-1571, src/kernels/bf16_gemm_v1.cu:2120-2126`
- risk: `Moderate. This path only covers the last 64 hot rows, so the upside is bounded, and a custom 64x384 epilogue specialization can easily trade barrier savings for extra register pressure or store-order bugs.`
- metrics to re-check: `end-to-end median runtime for 20260420_185423_bf16_gemm_v1_1181247 descendants, peeled 64x384 kernel gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct for the peeled kernel, launch__registers_per_thread for the peeled kernel, launch__shared_mem_per_block_allocated.sum for the peeled kernel, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct for the peeled kernel`

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
