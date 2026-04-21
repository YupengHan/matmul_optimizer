# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling`
- candidate id: `auto_diagnosis_round_045:dir_01`
- base run id: `20260421_083853_bf16_gemm_v1_4f123f5`
- primary family id: `legacy::port_grouped_row_traversal_into_the_non_ptx_128x128_sibling`
- planned action fingerprint: `restore_910beff_non_ptx_grouped_row_surface`
- selection mode: `recommended`
- source diagnosis id: `auto_diagnosis_round_045`
- round loop: `round 45/100`
- hypothesis: `The latest run is 24.411073 ms against an accepted anchor of 24.164272 ms. Round round 44/100 should replay the bounded `non_ptx_grouped` family once from the current state so the search keeps advancing instead of restoring forever.`
- expected bottleneck: `A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1700-1768, src/kernels/bf16_gemm_v1.cu:1890-1942, src/kernels/bf16_gemm_v1.cu:2107-2128`
- risk: `Moderate. This branch swaps the dominant hot-band dispatch away from the PTX winner, so it can regress meaningfully if the sibling surface is still under-tuned.`
- metrics to re-check: `end-to-end median runtime, hot-band gpu__time_duration.sum, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
