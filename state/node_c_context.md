# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_011652:dir_01`
- base run id: `20260421_011620_bf16_gemm_v1_4c6e7a1`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_011652`
- round loop: `round 27/100`
- hypothesis: `Round 26 answered the main question about the grouped-row non-PTX sibling: it is a stable alternate surface, but it does not break the plateau. Runtime recovered from 24.690687 ms to 24.183295 ms, yet the machine state came back almost exactly to the same 48.34%-tensor / 16.61%-warps / 5.49%-barrier / 7.23%-long-scoreboard envelope. That means the best next move is to restore the exact PTX winner again so the loop re-centers on the strongest measured anchor before it spends more rounds on tertiary surfaces.`
- expected bottleneck: `No new bottleneck is being attacked here; this is the exact recovery path back to the best measured correct surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1956-2060, src/kernels/bf16_gemm_v1.cu:2110-2127, src/kernels/bf16_gemm_v1.cu:156`
- risk: `Low. This is the exact best measured surface and the safest way to erase the residual gap between the current alternate surface and the recorded winner.`
- metrics to re-check: `end-to-end median runtime, correctness pass rate across all 3 cases, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`

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
