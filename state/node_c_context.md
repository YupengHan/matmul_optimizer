# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Shift The Hot-Band / Peeled Seam Down One More 256-Row Chunk`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_163723`
- round loop: `round 15/17`
- hypothesis: `Round 14/17 proved that the seam family is viable on top of the accepted PTX/export base: moving the pivot from 6400 to 6144 cut runtime from the failed broad control back down to 25.65470409 ms while keeping DRAM near 11.25 and long-scoreboard near 5.91. It still did not beat the accepted base, but it was the cleanest remaining direction. The next bounded step is to shift the pivot down one more 256-row chunk so the peeled path covers more of the bottom rows, without touching the PTX kernel internals or reopening any broad branch changes.`
- expected bottleneck: `Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-154, src/kernels/bf16_gemm_v1.cu:2097-2114`
- risk: `Medium. The seam family improved cleanly once, but moving too much work into the peeled path can eventually reverse that trend.`
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
