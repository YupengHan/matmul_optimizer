# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `restore accepted base, then narrow locality window`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_090253`
- round loop: `round 62/100`
- hypothesis: `Restore the accepted grouped_rows=8 + reversed row-pair + right-left PTX sweep + one-sync handoff base, then test whether reducing only kFixedHotBandPtxGroupedRows from 8 to 4 improves locality on the accepted consumer path without reopening the rejected grouped_rows=16 path.`
- expected bottleneck: `Hot-band consumer-path locality and reuse window width on the accepted PTX sweep / handoff path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:600-606, src/kernels/bf16_gemm_v1.cu:649-685, src/kernels/bf16_gemm_v1.cu:1407-1424, src/kernels/bf16_gemm_v1.cu:1934-1943`
- risk: `Medium: shrinking the group size may be too small and lose the locality benefit that the accepted base already captures, but the change stays narrowly scoped.`
- metrics to re-check: `kernel runtime versus 25.634208 ms, cp.async wait / CTA handoff stall behavior, shared-memory replay or load conflict signals, correctness against the BF16 reference`

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
