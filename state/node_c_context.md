# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Register-first PTX pair export that shrinks hot-band c_shared scratch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_171921`
- round loop: `single-run`
- hypothesis: `Round 3 made the key point for ranking: asymmetric handoff retime can recover from a bad branch by slashing mio, but it still lost to the accepted base because barrier and long-scoreboard both moved the wrong way. That says schedule-only retiming is mostly redistributing stalls, not removing work. The next highest-upside move inside the 64x384 PTX mainline is to attack the remaining export round-trip directly: keep the unchanged 64x96 tail and full-width hot-band compute, but push the paired export toward register-packed BF16 draining so the hot kernel depends less on float c_shared scratch and its warp-sync/export walk. Even a partial collapse of c_shared can cut LSU/shared traffic now and create real shared-memory headroom for deeper overlap later.`
- expected bottleneck: `Export-side shared traffic and scratch allocation are still taxing the hot-band kernel; they show up indirectly through LSU pressure, scoreboard exposure, and lack of real overlap headroom rather than through mio alone.`
- code locations: `src/kernels/bf16_gemm_v1.cu:42-60, src/kernels/bf16_gemm_v1.cu:212-229, src/kernels/bf16_gemm_v1.cu:301-315, src/kernels/bf16_gemm_v1.cu:442-495, src/kernels/bf16_gemm_v1.cu:869-873, src/kernels/bf16_gemm_v1.cu:950-956`
- risk: `Medium-high risk. A more direct export path can raise register pressure, complicate correctness, or fail to shrink shared usage enough to matter. It is still ranked first because it is materially different from the failed retime and helper-compaction families, and it offers both immediate payoff and a path to larger overlap changes later in the 20-round branch.`
- metrics to re-check: `launch__shared_mem_per_block_allocated, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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
