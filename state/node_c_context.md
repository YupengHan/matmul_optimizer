# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 1 Tiling: keep the 256x128/64x64 family, but add paired 64x64 export scratch to cut warp barrier tax`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_190126`
- round loop: `round 14/20`
- hypothesis: `The new tiling family is the real mainline now. Its first cut beat the previous accepted base by 2.4530878 ms and the hot 256x128 kernel changed the machine state in exactly the way a good structural pivot should: long scoreboard is down at 0.55, DRAM throughput is only 17.85, and tensor active is up to 37.63. That means the new family already solved the old memory-feed problem. The remaining taxes are local to the new kernel itself: barrier is still 20.76, short-scoreboard is 6.78, and the export path still serializes each 16x16 sub-tile through a single per-warp scratch tile with repeated __syncwarp. The most concrete next move is therefore to stay inside Human idea 1 and spend some of the 48 KB shared-memory budget headroom on a two-scratch export path for the 64x64 warp tile so the new family can reduce warp-local export/barrier overhead without changing its macro tiling.`
- expected bottleneck: `Warp-local export and synchronization overhead in the 256x128/64x64 kernel, now visible as high barrier stall and elevated short-scoreboard after memory starvation has already been fixed.`
- code locations: `src/kernels/bf16_gemm_v1.cu:80-105, src/kernels/bf16_gemm_v1.cu:664-709, src/kernels/bf16_gemm_v1.cu:1212-1297`
- risk: `This raises shared-memory usage in the pivot kernel. If the extra scratch is implemented clumsily, it could increase register pressure or fail to reduce sync density enough to matter. The change must stay local to the new 256x128 branch and not spill over into the stable 64x384 residual path.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__shared_mem_per_block_allocated, launch__registers_per_thread`

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
