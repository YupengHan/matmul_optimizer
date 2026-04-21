# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Grouped-Row Non-PTX 128x128 Sibling Surface`
- candidate id: `diagnosis_20260421_011427:dir_01`
- base run id: `20260421_011200_bf16_gemm_v1_2d59c53`
- primary family id: `legacy::port_grouped_row_traversal_into_the_non_ptx_128x128_sibling`
- planned action fingerprint: `restore_grouped_row_non_ptx_128x128_sibling_surface_from_910beff68055b974cfdbb268cda1087c8b44d665`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_011427`
- round loop: `round 26/100`
- hypothesis: `Round 25 gave the structural answer we needed from the auxiliary 256x128 family: the branch stayed correct, but runtime regressed to 24.690687 ms and the machine state stayed trapped at 48.23% tensor activity and 16.57% warps active. That is enough evidence to stop spending more immediate budget on this family. The best next move is therefore the strongest correctness-proven alternate surface already sitting in the frontier: the grouped-row non-PTX 128x128 sibling. It previously measured 24.178688 ms, which is inside the accepted-base noise band, while still replacing the PTX microkernel-specific control and export surface. That makes it the best round-26 recommendation: it recovers most of the round-25 loss without collapsing straight back into another same-surface PTX restore.`
- expected bottleneck: `PTX-microkernel-specific control and export coupling on the current winner surface, while preserving grouped-row locality and the same broad 128x128 footprint.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1844-1952, src/kernels/bf16_gemm_v1.cu:2070-2138, src/kernels/bf16_gemm_v1.cu:1870-1880`
- risk: `Low to medium. This is an exact restore of a measured-correct alternate surface, but its prior machine state was still plateau-like, so the main risk is spending one round to recover correctness and comparability without opening a new headroom signal.`
- metrics to re-check: `end-to-end median runtime, correctness pass rate across all 3 cases, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
