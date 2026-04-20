# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Apply Only A Minimal PTX Export Address Cleanup`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_160310`
- round loop: `round 7/17`
- hypothesis: `Round 6/17 kept correctness but still regressed to 25.77151966 ms, so the grouped-row window retune is now closed alongside the earlier prefetch and expanded B-shared-skew attempts. That leaves the narrowest surviving family on top of the accepted PTX base: a minimal export-address cleanup that does not reopen scratch lifetime, traversal direction, or shared-layout risk. Round 2/17 already showed that modest export cleanup can help, so the next best move is to trim only the remaining address setup in the PTX store helpers.`
- expected bottleneck: `Residual address-generation and store-helper overhead in the surviving PTX export path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:925-947, src/kernels/bf16_gemm_v1.cu:1008-1065, src/kernels/bf16_gemm_v1.cu:2044-2047`
- risk: `Low. The expected upside is smaller than a broader path switch, but it stays closest to the last accepted correct baseline and avoids reopening already closed families.`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
