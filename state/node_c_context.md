# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea async copy: split hot-band copy ownership so lower warps stage A and upper warps stage B`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_222312`
- round loop: `round 9/30`
- hypothesis: `The hot-band kernel still dominates and the current branch remains occupancy-limited but feed-sensitive. The user explicitly asked to keep pushing coalescing / async-copy ideas without falling back into the dedicated producer-only branch that already failed. A concrete middle ground is to keep all eight warps in the CTA and the same two-stage pipeline, but split copy ownership inside the staging helpers so the lower four warps own contiguous A stripes and the upper four warps own contiguous B stripes. That reduces simultaneous A/B copy traffic from every warp while avoiding permanent producer-only roles.`
- expected bottleneck: `Global-to-shared staging issue regularity and LSU pressure in the hot-band copy phase.`
- code locations: `src/kernels/bf16_gemm_v1.cu:stage_a_shared_tile_async, src/kernels/bf16_gemm_v1.cu:stage_b_shared_tile_async, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel`
- risk: `Moderate to high. This is intentionally narrower than the failed producer-only branch, but it still changes who issues the `cp.async` traffic and can regress if the participating half-warps become the new bottleneck.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
