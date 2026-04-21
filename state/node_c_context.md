# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Force 3-CTA Residency On The PTX 128x128 Hot Band`
- candidate id: `diagnosis_20260421_012211:dir_01`
- base run id: `20260421_012143_bf16_gemm_v1_803e749`
- primary family id: `aggressive::force_three_cta_residency_on_the_ptx_128x128_hot_band`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a_then_force_hot_band_launch_bounds_3`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_012211`
- round loop: `round 29/100`
- hypothesis: `The latest grouped_rows=8 regression makes the core plateau constraint explicit. The hot-band PTX kernel is still the dominant kernel at about 32.69 us, but it runs with 200 registers per thread, 22,016 B shared memory per block, only 2 resident CTAs per SM, and therefore only 8 active warps per SM or about 16.6% achieved warps. That is a structural latency-hiding wall, not a DRAM wall. The next move should therefore restore the exact 489574e PTX winner surface and then aggressively tighten the hot-band PTX branch around __launch_bounds__ and obvious live ranges so ptxas is forced to target 3-CTA residency. If that succeeds, the hot-band kernel can move from 8 toward 12 warps per SM without reopening the already-settled grouped_rows or export-order branches.`
- expected bottleneck: `Register-limited occupancy and latency hiding in the 128x128 PTX hot-band kernel, not global bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1955-2060, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Moderate. Correctness risk is low because the output ownership model stays on the proven PTX winner surface, but performance risk is real because forcing a tighter launch budget can introduce spills or expose a different barrier mix.`
- metrics to re-check: `end-to-end median runtime with a >0.15 ms improvement threshold over the current 24.517119 ms run, hot-band launch__registers_per_thread, hot-band launch__occupancy_limit_registers, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
