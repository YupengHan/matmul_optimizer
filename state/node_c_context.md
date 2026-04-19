# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Use a warp-local consumer-side B load swizzle on the peeled 64x384 hot path`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_124517`
- round loop: `round 4/5`
- hypothesis: `The restored 15d63b2 base still shows a hot-kernel signature consistent with shared/LSU pressure at the warp consumer boundary: tensor active is only 34.86 while mio_throttle stays at 35.53 with healthy 2-block occupancy, and the current B path still feeds WMMA through a simple single-skew shared layout. If B feed is attacked again, it must stay warp-local and consumer-side only: keep the existing single-skew producer path, keep `kCSharedStageCount = 2`, keep shared allocation at the accepted 46,592-byte hot-kernel level, and change only the warp read boundary with a lighter lane remap, XOR/interleaved swizzle, or hot-band-only explicit load path in `accumulate_peeled_shared_stage`. This explicitly rules out CTA-wide `repack_b_shared_tile()`-style work, extra B shared tiles, and any added CTA barrier.`
- expected bottleneck: `Warp-local shared-memory B-fragment reads and bank behavior in the 64x384 hot kernel, where the current consumer path may still be overfeeding LSU without requiring any macro-tile or CTA-pipeline rewrite.`
- code locations: `src/kernels/bf16_gemm_v1.cu:48-60, src/kernels/bf16_gemm_v1.cu:231-233, src/kernels/bf16_gemm_v1.cu:535-556, src/kernels/bf16_gemm_v1.cu:599-607`
- risk: `Even a warp-local swizzle can backfire if it silently increases lane address complexity or forces more shared instructions per fragment load. This direction is invalid if it increases `launch__shared_mem_per_block_allocated`, adds CTA barriers, or reduces `kCSharedStageCount` below 2.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
