# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted base, then test mirrored hot-band column sweep`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_085737`
- round loop: `round 60/100`
- hypothesis: `The 25.995744 ms regression came from the row-pair-dependent split column sweep. Restore the accepted grouped_rows=8 + reversed row-pair traversal + one-sync handoff baseline, then try a cleaner PTX hot-band variant that uses the mirrored column sweep uniformly for both row-pairs instead of branching the sweep by row-pair.`
- expected bottleneck: `Bad instruction-flow and locality interaction from the failed row-pair-dependent column split, rather than the accepted base traversal itself.`
- code locations: `src/kernels/bf16_gemm_v1.cu: grouped_rows=8 tile setup, src/kernels/bf16_gemm_v1.cu: reversed row-pair traversal loop, src/kernels/bf16_gemm_v1.cu: one-sync handoff sequence, src/kernels/bf16_gemm_v1.cu: hot-band column-order / PTX sweep logic`
- risk: `Moderate: the mirrored sweep may recover performance only if the accepted base is fully restored first; keep the row-pair-dependent split branch closed.`
- metrics to re-check: `kernel time vs 25.995744 ms, sm efficiency, branch divergence, shared-memory load/store balance, register pressure`

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
