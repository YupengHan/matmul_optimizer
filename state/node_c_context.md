# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Repair The 256x128 Half-Panel Register-Reuse Branch`
- candidate id: `diagnosis_20260421_005324:dir_01`
- base run id: `20260421_005058_bf16_gemm_v1_910beff`
- primary family id: `historical::repair_the_256x128_half_panel_register_reuse_branch`
- planned action fingerprint: `restore_half_panel_register_reuse_repair_surface_from_778a0b475a3fbcfd5a0f3fecc8381784fa832256`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_005324`
- round loop: `round 22/100`
- hypothesis: `Round 21 showed that the grouped-row non-PTX sibling is a valid alternate surface, but it did not open new headroom: it landed at 24.178688 ms, only 0.014416 ms behind the PTX best, while preserving essentially the same machine state at about 48.3% tensor activity, 16.6% active warps, 5.44% barrier stall, and 7.23% long scoreboard. Under the user's new rule, that means the search should stop rotating between near-tied plateau surfaces and instead spend a round on the one historical family that actually attacked the limiting resource. The half-panel 256x128 register-reuse branch is that family. Its best correctness-repair snapshot at commit 778a0b4 still failed correctness, but it preserved the only clear occupancy breakthrough in the repo: low-90s registers per thread, occupancy limit back to 2, active warps around 32.9%, and tensor activity above 43%. If the target is truly far below 24 ms, this is the right aggressive branch to rehydrate now.`
- expected bottleneck: `Register-limited occupancy and oversized live state on the wide hot-band family, which the plateaued PTX and sibling surfaces are no longer moving.`
- code locations: `src/kernels/bf16_gemm_v1.cu:23-345, src/kernels/bf16_gemm_v1.cu:345-1066, src/kernels/bf16_gemm_v1.cu:1580-1676`
- risk: `High. This is a historical repair branch with known correctness debt and broad kernel-surface drift, but it is also the only branch with evidence of a real occupancy-state change.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness pass rate across all 3 cases, end-to-end median runtime`

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
