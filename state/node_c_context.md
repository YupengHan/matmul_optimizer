# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Re-land the peeled hot kernel and trim the c_shared export path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_100543`
- round loop: `round 5/5`
- hypothesis: `Round 4 is the strongest evidence for the final round: the peeled fixed-shape hot kernel reached 37.373951 ms, only about 0.088 ms behind the accepted 37.285807 ms base, while improving tensor active from 32.61% to 34.58% and lowering barrier stall from 8.93% to 6.54%. The remaining gap now looks memory-side rather than control-flow-side: DRAM throughput rose to 50.65%, short scoreboard to 14.29%, and LSU requests to about 82.77%. The best one-round move on the restored base is therefore to re-land the peeled hot-path structure and pair it with a cheaper epilogue/export path so the win from the peeled steady-state loop is not handed back in the shared-to-global writeout.`
- expected bottleneck: `Epilogue-side shared/export traffic after the peeled steady-state loop improves control overhead.`
- code locations: `src/kernels/bf16_gemm_v1.cu:421-450 (current hot-loop region that the round-4 peeled specialization improved and would need to be re-landed), src/kernels/bf16_gemm_v1.cu:41-46 and src/kernels/bf16_gemm_v1.cu:454-485 (per-warp c_shared scratch and shared export path to trim), src/kernels/bf16_gemm_v1.cu:517-550 (fixed-shape dispatch path that should select the peeled hot kernel plus unchanged 64x96 tail)`
- risk: `This combines two moving pieces, so the implementation can regress if the peeled hot path is not re-landed cleanly or if the export simplification introduces layout/correctness bugs.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed`

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
