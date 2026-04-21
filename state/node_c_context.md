# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_002435:dir_01`
- base run id: `20260421_002405_bf16_gemm_v1_95723fb`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_ptx_surface_from_wait_and_hoist_drift`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_002435`
- round loop: `round 17/100`
- hypothesis: `Round 16 turned the current PTX control branch back into a net negative. The implementation changed only one new hot-band seam, but a source diff versus the best measured PTX commit `489574e` now shows two bounded drifts on the PTX winner surface: the round-15 future_tile_k hoist and the round-16 prologue wait retime. The latest run regressed from 24.17100811 ms to 24.19086361 ms even though barrier dipped slightly from 5.21% to 5.16%, because long-scoreboard widened back from 7.08% to 7.16% and the end-to-end result moved away from both the 24.17859173 ms accepted base and the 24.16427231 ms best-known run. The next move should therefore be to restore the best measured PTX surface before spending more rounds on alternate families.`
- expected bottleneck: `Source drift away from the proven PTX winner surface, specifically the prologue wait window and refill-address hot-band seam, not a need for another fresh PTX control experiment on top of the regressed variant.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2014-2022, src/kernels/bf16_gemm_v1.cu:2042-2054, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Low to moderate. This is a small, auditable restore onto the best measured PTX surface rather than a new speculative optimization.`
- metrics to re-check: `end-to-end median runtime versus the 24.190864 ms current run, the 24.178592 ms accepted base, and the 24.164272 ms best-known run, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum, correctness pass rate across all 3 cases`

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
