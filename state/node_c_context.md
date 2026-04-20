# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The Measured 64x384 Fixed-Main-Tile Control Path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_163231`
- round loop: `round 13/17`
- hypothesis: `Round 12/17 closes the grouping family for now: the 4-row retry was the best member of that family on the accepted export base, but tightening further to 2 rows regressed back to 26.06694412 ms and pushed DRAM up to 21.47. That means the local PTX-adjacent grouping lever has likely plateaued. The next best move is to reopen the older but directly measured `64x384` fixed-main-tile control path, which is the strongest remaining alternate family with explicit ranking evidence in the repo.`
- expected bottleneck: `Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1180-1248, src/kernels/bf16_gemm_v1.cu:2076-2116, src/kernels/bf16_gemm_v1.cu:151-159`
- risk: `Medium. The family has explicit sweep ancestry, but it is a broad branch change that can easily give back the wins from the accepted PTX/export base.`
- metrics to re-check: `correctness, median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__occupancy_limit_registers`

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
