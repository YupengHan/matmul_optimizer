# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted grouped_rows=8 hot-band consumer ordering`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_084642`
- round loop: `round 58/100`
- hypothesis: `The grouped_rows=16 branch was measured negative; returning to the accepted grouped_rows=8 window should recover the better PTX hot-band consumer behavior from round 56 and leave room for a narrower consumer-side tweak such as row-pair traversal order or another local ordering refinement.`
- expected bottleneck: `Consumer-side PTX hot-band ordering and export latency in bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, especially around the grouped-row dispatch and the consumer/export handoff.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1935-1944, src/kernels/bf16_gemm_v1.cu:1992-2008, src/kernels/bf16_gemm_v1.cu:1916-2015`
- risk: `Moderate: a local ordering tweak can easily drift back into the grouped_rows=16 slow path or disturb the accepted PTX export-scratch behavior.`
- metrics to re-check: `kernel runtime vs 24.713584 ms accepted base, dram throughput, long scoreboard stalls, achieved occupancy, sm efficiency`

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
