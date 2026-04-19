# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_02`
- direction name: `Full-width explicit PTX load-order follow-through without half-panel compute`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_140716`
- round loop: `round 5/5`
- hypothesis: `With barrier at 14.15 and mio at 2.32, the branch no longer looks primarily orchestration-bound. Long scoreboard is now the larger visible stall and compute-memory/DRAM throughput are already in the mid-50% range. A coherent next step inside the same 64x384 PTX branch is to push compute/load control further by replacing the remaining wrapper-style wmma.load/wmma.mma surface with a full-width explicit PTX dataflow, while explicitly avoiding the prechecked explicit mma.sync half-panel subpath that regressed. The point is to improve load order and fragment residency on the intact 12-tile hot band, not to split the tile into a separate 192-column compute path.`
- expected bottleneck: `Residual load-to-use latency and fragment feed ordering inside the PTX compute body, now that barrier and mio overhead are largely under control.`
- code locations: `src/kernels/bf16_gemm_v1.cu:261-299, src/kernels/bf16_gemm_v1.cu:388-402, src/kernels/bf16_gemm_v1.cu:801-818, src/kernels/bf16_gemm_v1.cu:915-948`
- risk: `This has more upside than dir_01 but is materially riskier in the last round. If the load-order rewrite drifts toward the old half-panel explicit mma.sync experiment, it can easily give back the steady progress from the last two rounds.`
- metrics to re-check: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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
