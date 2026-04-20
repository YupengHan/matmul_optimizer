# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the restored best surface and discard the split-ownership staging branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_222558`
- round loop: `round 10/30`
- hypothesis: `The split-ownership copy schedule is a clear dead end. It preserved correctness, but runtime regressed by about 0.48 ms, hot-band time regressed to about 41.96 us, registers exploded to about 222/thread, barrier stall rose to about 15.50%, and `mio_throttle` jumped to about 8.85%. That is exactly the kind of broad regression signal that should be reset immediately rather than debugged further. The first move is therefore to restore the pre-split surface before exploring another family.`
- expected bottleneck: `Not a new bottleneck attack; this is a branch reset after a strongly negative staging-ownership experiment.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Low. The restore is local and proven-correct. The only cost is one recovery round.`
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

- no tracked dirty paths at prepare time
