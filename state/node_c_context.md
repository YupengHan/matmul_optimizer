# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted-correct surface and try a light 4-column serpentine CTA swizzle on the hot-band grid`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_230948`
- round loop: `round 10/50`
- hypothesis: `Warp-local fragment-residency experiments have now failed correctness twice, so the next safe branch should move away from register choreography and toward cache locality. The user's L2 idea is the cleanest option: restore the accepted-correct implementation surface first, then apply a very light logical CTA swizzle that only reorders hot-band block_col mapping inside small groups. That keeps the inner microkernel untouched and tests whether the scheduler can get a little more B-tile locality from a serpentine launch order.`
- expected bottleneck: `Inter-CTA L2 locality across neighboring hot-band B tiles rather than warp-local tensor scheduling.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1, python scripts/graph.py restore-implementation --source-commit 0d78758`
- risk: `Moderate. The restore is low-risk, and the swizzle is intentionally lightweight, but the earlier heavier grouped traversal was negative.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band lts__throughput.avg.pct_of_peak_sustained_elapsed, runs/*/ncu_metrics.csv main 256x128 hot-band dram__throughput.avg.pct_of_peak_sustained_elapsed`

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
