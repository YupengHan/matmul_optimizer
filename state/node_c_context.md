# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `auto_diagnosis_round_095:dir_01`
- base run id: `20260421_084851_bf16_gemm_v1_96196d1`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `ptx_wait_commit_window_retime_without_replaying_closed_variants`
- selection mode: `recommended`
- source diagnosis id: `auto_diagnosis_round_095`
- round loop: `round 95/100`
- hypothesis: `The latest run is 24.634880 ms against an accepted anchor of 24.164272 ms. Round round 94/100 should replay the bounded `control_path` family once from the current state so the search keeps advancing instead of restoring forever.`
- expected bottleneck: `A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2008-2022, src/kernels/bf16_gemm_v1.cu:2042-2054, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. This branch stays on the PTX winner surface but its upside is measured in hundredths of a millisecond and the family is easy to over-replay.`
- metrics to re-check: `end-to-end median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
