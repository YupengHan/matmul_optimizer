# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Apply peeled steady-state only to the 8-warp 256x128 hot band and leave the residual 64x128 path on the proven generic loop`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_225949`
- round loop: `round 6/50`
- hypothesis: `Two rounds in a row show the same pattern: the main 256x128 hot-band kernel gets materially faster, but correctness fails. The most likely explanation is no longer 'steady-state peeling is wrong everywhere'; it is that the shared peeled schedule is valid for the dominant 8-warp hot-band kernel but not for the 2-warp residual 64x128 variant that was added in round 3. The next move should therefore split the behavior by TileConfig: keep the peeled steady-state on the main hot band where the win was measured, and restore the original generic per-tile control path on the residual kernel to see whether correctness returns without giving back the main-kernel gain.`
- expected bottleneck: `Main hot-band control overhead is still the target, but correctness risk is likely concentrated in the smaller residual 64x128 variant rather than the dominant 256x128 kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_64x64_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Moderate and well-bounded. This is a surgical split of a winning-but-incorrect schedule, not a new pipeline family.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv residual 64x128 hot-band gpu__time_duration.sum, runs/*/ncu_metrics.csv main 256x128 hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
