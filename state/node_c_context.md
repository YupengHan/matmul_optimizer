# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_02`
- direction name: `Restore the last correct round-2 branch `06eedc6` and continue from the validated streaming-B + B-lookahead surface`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_220618`
- round loop: `round 4/30`
- hypothesis: `If the A-side lookahead cannot be repaired quickly, the right fallback is to stop paying correctness risk and restore the last correct branch. Round 2 already recovered the streaming-B branch and added the one-fragment B-side Ps2r lookahead while keeping correctness. Resetting there preserves the strongest valid exploratory surface for the remaining rounds instead of continuing from a broken commit.`
- expected bottleneck: `Not a direct micro-bottleneck attack; this is a branch repair to recover a correctness-valid baseline before the next experiment.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Low. This is a known-good restore, but it spends a round on recovery rather than on a new ceiling-raising idea.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread`

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
