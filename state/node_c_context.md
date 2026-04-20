# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted grouped_rows=8 base, then test 8->6 hot-band narrowing`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_091413`
- round loop: `round 64/100`
- hypothesis: `The accepted grouped_rows=8 + reversed row-pair + right-left PTX sweep + one-sync handoff + unroll 2 base is still the best locality shape, and the remaining question is whether a narrower kFixedHotBandPtxGroupedRows value of 6 preserves enough reuse without reintroducing the DRAM growth seen at grouped_rows=4.`
- expected bottleneck: `Locality loss in the hot-band PTX consumer ordering and row reuse window, not the broader sweep or sync structure.`
- code locations: `src/kernels/bf16_gemm_v1.cu:kFixedHotBandPtxGroupedRows, src/kernels/bf16_gemm_v1.cu:kFixedHotBandUnroll, src/kernels/bf16_gemm_v1.cu:grouped_rows=8 accepted base path, src/kernels/bf16_gemm_v1.cu:right-left PTX sweep and one-sync handoff`
- risk: `If 6 is too narrow, it may recover less reuse than 8 while still missing the DRAM amplification seen with grouped_rows=4; however it is the cheapest remaining locality change on the accepted base.`
- metrics to re-check: `runtime_ms versus 25.934336 ms, DRAM throughput / traffic, L2 hit rate, achieved occupancy, warp stall mix around the handoff`

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
