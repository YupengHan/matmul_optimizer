# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the round-8 streaming-B branch before continuing exploration`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_215124`
- round loop: `round 1/30`
- hypothesis: `The current implementation surface is a dead-end final-round producer-only staging experiment. Restoring the round-8 streaming-B branch puts the code back on the last recent branch that improved runtime and feed-side metrics without increasing registers or shared memory. That branch is the right exploratory anchor if the next 29 rounds are meant to compound one family rather than wander across already-falsified ideas.`
- expected bottleneck: `Not a micro-bottleneck change; this is a branch reset to remove a clearly negative orchestration experiment and recover the last good B-feed baseline.`
- code locations: `src/kernels/bf16_gemm_v1.cu`
- risk: `Low. This is a known-correct restore to a recently measured branch. The only risk is spending one round on recovery, but continuing from the current 222-register branch is less credible.`
- metrics to re-check: `correctness, median runtime, runs/*/ncu_details.csv hot-band gpu__time_duration.sum, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
