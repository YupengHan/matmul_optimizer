# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `auto_diagnosis_round_070:dir_01`
- base run id: `20260421_084440_bf16_gemm_v1_dc6802e`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a`
- selection mode: `recommended`
- source diagnosis id: `auto_diagnosis_round_070`
- round loop: `round 70/100`
- hypothesis: `The latest measured run landed at 24.446976 ms, still +0.282703 ms away from the accepted 24.164272 ms anchor. The fastest way to keep the loop grounded is to replay the exact accepted PTX surface before reopening another branch.`
- expected bottleneck: `Search drift away from the accepted PTX steady state rather than a missing structural opportunity.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:2000-2060, src/kernels/bf16_gemm_v1.cu:2107-2128`
- risk: `Low. This is the known accepted PTX anchor surface.`
- metrics to re-check: `end-to-end median runtime, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Implementation notes

- implement exactly one selected direction
- stay within the primary family by default
- if the implementation clearly crosses into another family, update `state/active_direction.json` and record `secondary_family_ids` before finalize
- if the implementation semantically drifts from the planned action, update `implemented_action_fingerprint`, `semantic_delta_tags`, or `actual_code_regions` in `state/active_direction.json` before finalize
- build failure is still recorded as a structured `state/latest_attempt.json` entry with `build_status=FAIL`

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
