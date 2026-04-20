# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 10 Stage: keep the corrected 3-stage hot band, but squeeze it under the 128-reg cliff`
- selection mode: `recommended`
- source diagnosis id: `node_b_20260419_181340_round09_512448e`
- round loop: `round 9/20`
- hypothesis: `Round 8 is the first correct 3-stage result, and the machine-level shift is too large to dismiss: barrier dropped from 14.30 to 4.60, long scoreboard from 6.21 to 1.21, mio from 2.30 to 0.71, registers/thread from 167 to 132, and shared/block from 46.6 KB to 44.8 KB. That says the Stage family is real, but it is not yet cashing out into runtime because tensor issue stayed middling and occupancy is still pinned at 1 block/SM. The next move should stay inside Idea 10 and target the concrete cliff that is now close enough to matter: trim stage/export bookkeeping live ranges so the hot 64x384 PTX kernel can get from 132 regs/thread to 128 or below without giving back the new low-stall signature. If that works, the Stage family finally has a plausible path to convert overlap into more resident work and real runtime wins.`
- expected bottleneck: `launch__occupancy_limit_registers and residual tensor underfill after overlap gains; short scoreboard is the next stall to watch once barrier, long scoreboard, and mio are already low.`
- code locations: `src/kernels/bf16_gemm_v1.cu:410-500, src/kernels/bf16_gemm_v1.cu:862-896, src/kernels/bf16_gemm_v1.cu:939-1014`
- risk: `If the live-range split is attempted by adding helper state or extra fences, ptxas can re-inflate registers or erase the Stage-family overlap win. If this branch still cannot clear the 128-reg cliff, it loses its best concrete reason to continue as the primary family.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, median runtime`

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
