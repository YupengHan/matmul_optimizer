# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Bound The 128x128 Two-Stage Feed Cadence`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_120042`
- round loop: `round 82/100`
- hypothesis: `The paired PTX export helper is now closed-negative, but the 128x128 two-stage sibling is still the best distinct family from the improved baseline. A bounded adjustment to its cp.async cadence, wait-group timing, or shared-memory handoff may trim the new long-scoreboard cost without bringing back the DRAM or barrier inflation that hurt the closed variants.`
- expected bottleneck: `Feed latency and stage handoff inside the 128x128 two-stage kernel, with the long-scoreboard rise indicating that the current baseline is still waiting too long on data readiness.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1822-1920, src/kernels/bf16_gemm_v1.cu:2044-2111`
- risk: `Medium. This family already proved it can move the profile in the right direction, but the remaining gap may be a hard local limit rather than a scheduling issue.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed, launch__occupancy_limit_registers`

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
