# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Shift The Hot-Band / Peeled Seam Down By One PTX Block`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_163459`
- round loop: `round 14/17`
- hypothesis: `Round 13/17 closed the 64x384 control decisively: runtime exploded to 33.9645443 ms, DRAM hit 55.24, and barrier reached 17.01, so the broad fixed-main-tile branch is not competitive. That leaves the seam between the accepted PTX hot-band kernel and the peeled 384-row band as the cleanest remaining bounded lever. The next step should shift `kFixedPivotHotRows` down by one 128-row PTX block so the peeled path absorbs more of the bottom rows, without changing the PTX kernel internals themselves.`
- expected bottleneck: `Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-154, src/kernels/bf16_gemm_v1.cu:2097-2114`
- risk: `Medium. The change is very narrow, but moving the seam may simply shift work into the slower peeled path instead of reducing the handoff cost.`
- metrics to re-check: `correctness, median runtime, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
