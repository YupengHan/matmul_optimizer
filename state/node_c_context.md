# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_014129:dir_01`
- base run id: `20260421_014052_bf16_gemm_v1_7296bf2`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_014129`
- round loop: `round 33/100`
- hypothesis: `Round 29 through round 32 are now enough evidence to step off the forced-3-CTA 128x128 family and recover. The PTX launch-bounds probe and the non-PTX sibling launch-bounds probe both converged on the same answer: they lowered the hot-band register budget to 168, raised achieved warps to about 24.7%, and collapsed long-scoreboard stalls, but they also pushed barrier stall to roughly 11% and regressed runtime into the mid-20s. That means the loop should return to the exact 489574e PTX anchor now so the next aggressive branch starts from the best correctness-proven base instead of from a measured loss.`
- expected bottleneck: `Known register-limited plateau on the accepted PTX hot-band surface, used here as a recovery anchor.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1955-2060, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Low. This is the clean recovery path.`
- metrics to re-check: `end-to-end median runtime versus the current 26.398208 ms run, hot-band gpu__time_duration.sum, hot-band launch__registers_per_thread, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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

- `src/kernels/bf16_gemm_v1.cu`
