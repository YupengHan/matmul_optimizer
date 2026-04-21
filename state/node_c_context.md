# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 256x128 Pivot Hot-Band Kernel`
- candidate id: `auto_diagnosis_round_091:dir_01`
- base run id: `20260421_084810_bf16_gemm_v1_4cd499c`
- primary family id: `aggressive::transplant_half_panel_register_budget_into_the_correct_256x128_pivot`
- planned action fingerprint: `restore_correct_256x128_pivot_surface_then_transplant_low_reg_half_panel_staging_without_writer_split`
- selection mode: `recommended`
- source diagnosis id: `auto_diagnosis_round_091`
- round loop: `round 91/100`
- hypothesis: `The latest run is 24.619967 ms against an accepted anchor of 24.164272 ms. Round round 90/100 should replay the bounded `pivot_256x128` family once from the current state so the search keeps advancing instead of restoring forever.`
- expected bottleneck: `A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1580-1670, src/kernels/bf16_gemm_v1.cu:2107-2128, src/kernels/bf16_gemm_v1.cu:2130-2135`
- risk: `High. This branch materially changes the dominant hot-band geometry and has historically carried large regression risk.`
- metrics to re-check: `end-to-end median runtime, launch__registers_per_thread, launch__shared_mem_per_block_allocated, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`

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
