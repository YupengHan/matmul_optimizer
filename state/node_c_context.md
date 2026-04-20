# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Try the 256x128 hot-band CTA with 64x64 warp tiles on top of the proven K16 stage contract`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_000002`
- round loop: `round 18/50`
- hypothesis: `The corrected 128x128 K16 branch is our current best result, while the 128x128x32 branch proved that making the pipeline deeper is not enough and actually hurt active warps. That shifts the next priority toward the user's explicit tiling idea: a 256x128 CTA with the same 64x64 warp tile. This keeps the proven K16 double-buffer contract, keeps wide cp.async staging and shared-memory reuse intact, and increases the hot-band CTA to eight warps so the kernel can test whether more in-flight warps recover tensor issue without reopening the stage-race problem.`
- expected bottleneck: `CTA shape and active-warps pressure in the hot-band kernel, not deeper staging. The target is to improve warp residency and tensor issue while retaining the already-correct async-copy pipeline.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1366, src/kernels/bf16_gemm_v1.cu:1423, src/kernels/bf16_gemm_v1.cu:1754`
- risk: `The 256x128 CTA may increase shared or register pressure enough to offset the extra warps. It likely needs the same consume-before-overwrite fence as the corrected 128x128 K16 path, otherwise the old stage race may simply reappear in a larger block.`
- metrics to re-check: `correctness pass rate on all benchmark cases, median runtime, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
