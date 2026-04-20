# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: stream the 64x64 PTX micro-tile by row-pairs and export each completed pair through the new paired scratch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_190621`
- round loop: `round 15/20`
- hypothesis: `Round 14 proved the new 256x128/64x64 tiling family is still the right mainline, but it also changed what the next limiter is. Paired export improved runtime by another 0.91182423 ms even though barrier stayed flat at 20.89 and registers stayed flat at 166. The meaningful metric movement was long scoreboard 0.55 -> 0.22 and short scoreboard 6.78 -> 6.64. That says the paired-scratch win came from shortening the warp-local export and dependency chain, not from removing the main-loop CTA barrier. The right follow-up is therefore not another generic barrier chase. It is to cash in the new paired export structure by shrinking the live accumulator and fragment footprint: compute the 64x64 warp tile as row-pairs, then immediately store and export each completed row-pair through the existing two-stage c_shared scratch before reusing those accumulator registers for the next row-pair. This stays inside the accepted 256x128/64x64 family while finally attacking the unchanged 166-register occupancy wall.`
- expected bottleneck: `Register and warp-local dependency pressure inside the 64x64 PTX microkernel, which now appears more important than headline CTA barrier rate.`
- code locations: `src/kernels/bf16_gemm_v1.cu:513-568, src/kernels/bf16_gemm_v1.cu:690-741, src/kernels/bf16_gemm_v1.cu:1235-1329`
- risk: `This is more invasive than the paired-export change. If the row-pair schedule reloads A or B fragments too aggressively, tensor issue can fall or long scoreboard can come back. The implementation also has to avoid inserting extra warp syncs that erase the gain.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
