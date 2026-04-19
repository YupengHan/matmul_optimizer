# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reduce cp.async barrier pressure`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_210931`
- round loop: `round 2/5`
- hypothesis: `The new profile shifted away from long-scoreboard latency and toward synchronization overhead. A less stop-and-go prefetch schedule, with fewer or better-placed waits in the K loop, should reduce the 21.89% barrier stall and let the tensor pipe stay busier.`
- expected bottleneck: `Barrier and wait-group serialization in the double-buffered steady-state loop.`
- code locations: `src/kernels/bf16_gemm_v1.cu:44-53, src/kernels/bf16_gemm_v1.cu:113-177`
- risk: `Moderate. Reordering the cp.async pipeline can introduce correctness bugs or remove useful overlap if the new schedule is too shallow.`
- metrics to re-check: `smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__throughput.avg.pct_of_peak_sustained_elapsed, median runtime`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
