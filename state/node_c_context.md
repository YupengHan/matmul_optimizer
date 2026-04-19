# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Phased 64x384 micro-panels to shrink the live set`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260419_093742`
- round loop: `round 2/5`
- hypothesis: `Keep the autotune-selected 64x384 outer CTA, but stop carrying the full 12-wide B and accumulator live set through the hot loop. The latest regressed run still sits at 126 registers/thread, occupancy limit 2, and only 32.95% active warps with tensor active down at 28.22%, so the best next move on the restored accepted base is to serialize the 384-wide work into smaller internal micro-panels such as 2x192 or 3x128 while preserving the 384-wide CTA-count advantage.`
- expected bottleneck: `Register-limited occupancy and weak latency hiding from the 12-fragment live set in the hot 64x384 loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:32-39 (TileConfig shape parameters, especially kWarpMmaTilesN and kTensorBlockN), src/kernels/bf16_gemm_v1.cu:399-445 (warp tile mapping plus accumulator and B-fragment residency in the hot loop), src/kernels/bf16_gemm_v1.cu:517-550 (fixed-shape launch path that should keep the 64x384 outer tile and 64x96 tail split)`
- risk: `Serial micro-panels can give back some of the 64x384 CTA-count win if extra panel boundaries, reloads, or control flow add too much instruction overhead.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
