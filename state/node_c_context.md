# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Force 3-CTA Residency On The Non-PTX 128x128 Sibling`
- candidate id: `diagnosis_20260421_013852:dir_01`
- base run id: `20260421_013804_bf16_gemm_v1_b8a113b`
- primary family id: `aggressive::force_three_cta_residency_on_the_non_ptx_128x128_sibling`
- planned action fingerprint: `restore_grouped_row_non_ptx_128x128_sibling_surface_from_910beff68055b974cfdbb268cda1087c8b44d665_then_force_launch_bounds_3`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_013852`
- round loop: `round 32/100`
- hypothesis: `The current PTX anchor is fast but structurally pinned at 200 registers, occupancy_limit_registers=2, and about 16.62% active warps. The round-29 PTX launch-bounds probe showed that forcing 3-CTA residency can move the machine state materially, but it also exposed a PTX-specific barrier pathology. The non-PTX 128x128 sibling is the cleanest next branch to carry that occupancy experiment because it is already a correctness-proven alternate surface at 24.183295 ms and starts slightly leaner at 196 registers with nearly the same plateau signature. Restoring the exact sibling surface and then forcing its hot-band kernel toward 3 resident CTAs is therefore the best bounded aggressive test: it asks whether the occupancy win survives better on the non-PTX control/export path than it did on the PTX microkernel path.`
- expected bottleneck: `Register-limited occupancy and latency hiding on the non-PTX 128x128 sibling surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1842-1954, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Moderate. Correctness risk is low because the base sibling surface is already known-good, but performance risk remains because forcing a 3-CTA budget can still trade registers for spills or expose new synchronization costs.`
- metrics to re-check: `end-to-end median runtime with a >0.15 ms improvement threshold over the current 24.168880 ms run, hot-band launch__registers_per_thread, hot-band launch__occupancy_limit_registers, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band gpu__time_duration.sum`

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
