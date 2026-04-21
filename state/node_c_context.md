# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling`
- candidate id: `diagnosis_20260421_003952:dir_01`
- base run id: `20260421_003751_bf16_gemm_v1_a64efce`
- primary family id: `legacy::port_grouped_row_traversal_into_the_non_ptx_128x128_sibling`
- planned action fingerprint: `restore_grouped_row_non_ptx_128x128_sibling_surface_from_78421da`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_003952`
- round loop: `round 21/100`
- hypothesis: `Round 20 proved that the current aggressive move should not be another blind 256x128 geometry promotion: the hot-band kernel itself regressed from the PTX winner's 32.687 us to 43.097 us while tensor activity dropped from 48.39% to 36.77% and register occupancy collapsed from limit=2 back to limit=1. The best next move is therefore not another tiny PTX-local retime, but the closest evidence-backed alternate surface already in history: the grouped-row non-PTX 128x128 sibling. That branch previously measured 24.180737 ms with a 32.697 us hot-band kernel, essentially tied with the PTX winner inside the current noise band, while still changing the control/export surface materially enough to qualify as a real alternate family rather than a restore.`
- expected bottleneck: `PTX-microkernel-specific control/export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1855-1946, src/kernels/bf16_gemm_v1.cu:1970-2060, src/kernels/bf16_gemm_v1.cu:2081-2091`
- risk: `Medium. This is a real surface pivot, but it is a measured-correct one that already stayed inside the 24.16-24.18 ms band instead of opening another multi-millisecond regression.`
- metrics to re-check: `end-to-end median runtime versus the 24.164272 ms PTX best and the 30.136320 ms round-20 source run, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
