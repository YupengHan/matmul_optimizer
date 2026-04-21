# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure`
- candidate id: `diagnosis_20260420_222929:dir_01`
- base run id: `20260420_222846_bf16_gemm_v1_8ba4496`
- primary family id: `legacy::flatten_ptx_hot_band_compute_helpers_to_reduce_register_pressure`
- planned action fingerprint: `00ef6081291d54f2`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_222929`
- round loop: `round 6/20`
- hypothesis: `The round-5 control-path tweak effectively held runtime flat while leaving the same occupancy-limited signature in place: the hot PTX kernel still reports only 16.49% active warps and the same register-limited CTA ceiling. That makes register pressure the most coherent next family. The historically rehydrated helper-flattening branch already showed a 24.696832 ms run, and the current profile still supports its thesis that the PTX helper structure is keeping too much live state around the active 128x128 hot-band path.`
- expected bottleneck: `Register-limited occupancy and weak latency hiding caused by helper-induced live ranges in the PTX hot-band compute path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-855, src/kernels/bf16_gemm_v1.cu:1144-1210, src/kernels/bf16_gemm_v1.cu:1911-1946`
- risk: `Medium. Helper flattening is still bounded to the active PTX branch, but it can devolve into a no-op if ptxas keeps the same live ranges and scheduling.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, end-to-end median runtime versus the 24.177664 ms accepted base`

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
