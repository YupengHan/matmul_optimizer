# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260420_224213:dir_01`
- base run id: `20260420_224147_bf16_gemm_v1_df5bac2`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `8e91e546243f09ff`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_224213`
- round loop: `round 8/100`
- hypothesis: `Round 7/100 proved that the bounded PTX export-address cleanup is still live on top of the restored grouped-rows-4 PTX surface: runtime improved from 24.180656 ms to a new best custom 24.164352 ms with correctness intact. But the gain was only 0.016304 ms, small enough that the search policy still tagged it PASS_FLAT and left the accepted base unchanged. The counters also say the export family is nearing saturation rather than exposing a fresh win path: barrier only nudged down from 5.48 to 5.42, long-scoreboard ticked up from 7.17 to 7.26, and active warps stayed pinned at 16.62. That makes the still-open PTX control-path family the best next move, because it keeps the restored surface and the cleaned export helper but attacks the remaining inner-loop control / consume-order overhead that the narrow export cleanup could not fully remove.`
- expected bottleneck: `Residual PTX hot-band control-path overhead and scoreboard / barrier balance on the restored grouped-rows-4 PTX surface, not another export-address-only cleanup.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-804, src/kernels/bf16_gemm_v1.cu:1005-1075, src/kernels/bf16_gemm_v1.cu:1981-2062`
- risk: `Moderate. This family is still live and remains the top frontier representative, but another too-small control-order nudge can easily collapse back into sub-threshold noise on an already good PTX base.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms new-best control run, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__registers_per_thread, hot-band gpu__time_duration.sum`

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
