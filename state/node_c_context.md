# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_013500:dir_01`
- base run id: `20260421_013416_bf16_gemm_v1_17032e6`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_013500`
- round loop: `round 31/100`
- hypothesis: `Round 29 and round 30 spent two consecutive rounds on the occupancy-first 128x128 branch and extracted the information we needed. The launch-bounds-only probe proved that the hot-band PTX kernel can be pushed down to 168 registers and up to 24.77% active warps, but it paid for that with a barrier wall. The two-K-stage follow-on then tried to amortize those barriers, but its 43,008 B shared-memory footprint collapsed active warps back to 16.58% and pushed runtime out to 28.20 ms. At this point the branch has consumed its immediate budget. The correct next move is to restore the exact 489574e PTX winner so the search returns to the best correctness-proven surface before it tries the next aggressive family.`
- expected bottleneck: `Known register-limited plateau on the accepted 128x128 PTX surface, used here as a recovery anchor rather than a discovery move.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1955-2060, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Low. This is the safe recovery path after two measured regressions.`
- metrics to re-check: `end-to-end median runtime versus the current 28.200448 ms run, hot-band gpu__time_duration.sum, hot-band launch__registers_per_thread, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
