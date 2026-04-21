# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering`
- candidate id: `auto_diagnosis_round_073:dir_01`
- base run id: `20260421_084511_bf16_gemm_v1_634ee7b`
- primary family id: `legacy::restore_accepted_grouped_rows_8_hot_band_consumer_ordering`
- planned action fingerprint: `restore_grouped_rows_8_consumer_ordering_anchor_replay`
- selection mode: `recommended`
- source diagnosis id: `auto_diagnosis_round_073`
- round loop: `round 73/100`
- hypothesis: `The latest run is 24.420304 ms against an accepted anchor of 24.164272 ms. Round round 72/100 should replay the bounded `grouped_rows8` family once from the current state so the search keeps advancing instead of restoring forever.`
- expected bottleneck: `A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:1956-2060, src/kernels/bf16_gemm_v1.cu:1983-1993`
- risk: `Moderate to high. This branch changes CTA grouping and consumer locality and already has historical loss evidence, so it should stay bounded to an exact replay surface.`
- metrics to re-check: `end-to-end median runtime, hot-band gpu__time_duration.sum, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
