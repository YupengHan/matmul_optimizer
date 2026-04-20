# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the best surface and replace the last 64 hot rows with a dedicated 64x128 residual PTX kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_223942`
- round loop: `round 3/50`
- hypothesis: `The recent hot-band micro-tuning attempts are mostly noise or regressions, and the latest best custom still comes from the restored pre-experiment surface. The largest untouched structural opportunity is no longer inside the 256x128 hot-band body, but in the last 64 hot rows that still fall back to the 384-wide peeled kernel. Those rows match one 64x128 warp-local PTX tile perfectly, so a dedicated residual-hot-band kernel can keep the same 64x64 warp microkernel and export path while avoiding the heavier 384 peeled path for that final strip.`
- expected bottleneck: `Residual hot-row overhead from routing the last 64 rows through the generic 384 peeled kernel instead of a matching fixed-shape PTX path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:FixedHotBandTile256x128, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, src/kernels/bf16_gemm_v1.cu:launch_bf16_gemm_v1`
- risk: `Moderate to high. This is a larger structural change than the recent local tweaks, but it reuses the existing hot-band PTX machinery instead of inventing a new microkernel family.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, runs/*/ncu_details.csv peeled kernel gpu__time_duration.sum, launch__registers_per_thread, launch__shared_mem_per_block_allocated`

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
