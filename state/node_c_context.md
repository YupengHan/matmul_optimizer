# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_003229:dir_01`
- base run id: `20260421_003148_bf16_gemm_v1_5188311`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_ptx_surface_after_grouped_rows_8_regression`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_003229`
- round loop: `round 19/100`
- hypothesis: `Round 18 provided clean negative evidence on the grouped_rows=8 alternate PTX surface. Runtime jumped from 24.17296028 ms to 24.53401566 ms, long-scoreboard widened from 7.13% to 7.33%, and the branch fell far outside the current 24.16-24.18 band. The source change for this round was intentionally narrow, so the loop should not stack another new family on top of the bad state. The next move should be to restore the PTX winner surface again, re-anchor the search on the known-good grouped_rows=4 implementation, and only then spend further rounds on alternate geometry or sibling-surface families.`
- expected bottleneck: `The grouped_rows=8 locality regime itself is the measured problem here; the immediate need is to remove that drift and recover the proven PTX winner surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:1979-1993, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Low to moderate. This is a narrow restore from a clearly negative branch rather than a fresh speculative change.`
- metrics to re-check: `end-to-end median runtime versus the 24.534016 ms current run, the 24.178592 ms accepted base, and the 24.164272 ms best-known run, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum, correctness pass rate across all 3 cases`

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
