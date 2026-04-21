# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep 3-CTA Residency And Amortize Barriers With Two-K Stages`
- candidate id: `diagnosis_20260421_013125:dir_01`
- base run id: `20260421_013042_bf16_gemm_v1_bb69e9b`
- primary family id: `aggressive::keep_three_cta_residency_and_amortize_barriers_with_two_k_stages`
- planned action fingerprint: `keep_grouped_rows4_and_three_cta_budget_then_route_default_hot_band_to_128x128x32_kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_013125`
- round loop: `round 30/100`
- hypothesis: `Round 29 proved that the occupancy-first idea was directionally correct even though the end-to-end runtime regressed. The hot-band PTX branch dropped from 200 to 168 registers per thread, moved occupancy_limit_registers from 2 to 3, raised achieved warps from 16.59% to 24.77%, and collapsed long-scoreboard stall from 7.34% to 1.69%. The regression came from a new synchronization wall instead: barrier stall jumped from 5.19% to 10.97% and the hot-band kernel slowed to about 33.76 us. The cleanest next move is therefore not to undo the occupancy gain, but to keep the grouped_rows=4 and 3-CTA residency budget while routing the default hot-band launch onto the existing 128x128x32 two-K-stage kernel so each steady-state barrier protects two K tiles instead of one.`
- expected bottleneck: `Synchronization and stage handoff overhead after the residency wall has been partially relaxed.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1685-1841, src/kernels/bf16_gemm_v1.cu:1955-2060, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Moderate. This is still inside the same occupancy-first branch and should preserve correctness semantics more cleanly than reopening 256x128 ownership work, but it can easily give back the register win if the two-K-stage kernel compiles much fatter than expected.`
- metrics to re-check: `end-to-end median runtime with a >0.15 ms improvement threshold over the current 25.911183 ms run, hot-band launch__registers_per_thread, hot-band launch__occupancy_limit_registers, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band gpu__time_duration.sum`

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
