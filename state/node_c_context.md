# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_03`
- direction name: `Restore the pre-sweep best surface without adding a new experiment`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_221835`
- round loop: `round 8/30`
- hypothesis: `If the loop needs to recover immediately before spending another experimental round, the safest move is simply to restore the pre-sweep best custom surface. This keeps the remaining rounds anchored on the best measured family and discards the proven-negative `Right Left Right Left` order.`
- expected bottleneck: `Not a direct bottleneck attack; this is a branch repair after a negative warp-local consumer experiment.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Low. The restore is simple and correctness-stable, but it spends a round on recovery rather than on a new idea.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum`

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
