# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the new best custom branch `5dd9f0d` and discard the grouped-CTA traversal`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_221410`
- round loop: `round 6/30`
- hypothesis: `Round 5 cleanly falsified the L2-launch-order clue as an implementation branch. The grouped traversal kept correctness, slightly improved the hot-band kernel to about 40.70 us, and even nudged headline tensor activity up, but overall runtime regressed from 29.432832 ms to 30.692336 ms. That means the remap is not a viable surface for the next 25 rounds even if one sub-kernel metric looks nicer. The first move should therefore be to restore the correctness-valid best custom branch `5dd9f0d` before trying another family.`
- expected bottleneck: `Not a new bottleneck attack; this is a branch reset after a structurally negative CTA-traversal experiment.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Low. The restore is local and measured. The only cost is one recovery round, but continuing from the slower grouped-traversal branch is less defensible.`
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
