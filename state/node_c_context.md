# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Register-first PTX export follow-through on the hot band`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_140002`
- round loop: `round 4/5`
- hypothesis: `The PTX branch has now delivered three consecutive wins, and round 3 specifically showed that orchestration/barrier cleanup is paying off: runtime is down to 33.366 ms, barrier is 14.34, and mio is only 2.31. The hot 64x384 kernel still exits through the shared export surface at src/kernels/bf16_gemm_v1.cu:301-315, :405-439, and :894-896, which means the branch still materializes every accumulator tile through shared before BF16 packing. With control/orchestration already improved, the best next step is to make the hot-band PTX branch own export as well: retire accumulator tiles from registers more directly so shared LSU work, short scoreboard, and export-side live state all shrink while leaving the 64x96 tail untouched.`
- expected bottleneck: `The remaining cost has shifted away from barrier and mio tax toward export-side shared/LSU work and residual register lifetime in the hot-band epilogue.`
- code locations: `src/kernels/bf16_gemm_v1.cu:212-229, src/kernels/bf16_gemm_v1.cu:301-315, src/kernels/bf16_gemm_v1.cu:405-439, src/kernels/bf16_gemm_v1.cu:813-817, src/kernels/bf16_gemm_v1.cu:894-896`
- risk: `Direct register export changes accumulator-to-output mapping and BF16 packing at the same time, so correctness risk is real. It also may not flip occupancy_limit_registers by itself if the dominant register cost is still the 12-tile accumulator residency.`
- metrics to re-check: `l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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
