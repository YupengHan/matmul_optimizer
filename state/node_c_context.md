# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Re-anchor exactly at the accepted best implementation commit 0d78758 before more experiments`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_230527`
- round loop: `round 8/50`
- hypothesis: `The loop has now spent several rounds on variants that are either incorrect or clearly slower than the accepted best surface. The current correct branch is 30.55 ms, while the accepted best measured implementation at commit 0d78758 already delivered 29.33 ms. Continuing to optimize on a degraded surface will make future measurements harder to interpret. The highest-value next move is therefore a clean implementation restore to 0d78758 so the next experimental branches start again from the real accepted baseline.`
- expected bottleneck: `Not a bottleneck attack. This is a reset to the fastest correct implementation surface before the next human-idea experiments.`
- code locations: `src/kernels/bf16_gemm_v1.cu, python scripts/graph.py restore-implementation --source-commit 0d78758`
- risk: `Low. This uses a repo-supported restore path and should only roll back implementation drift, not benchmark state or unrelated documentation edits.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_metrics.csv main 256x128 hot-band gpu__time_duration.sum`

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
