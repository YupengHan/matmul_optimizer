# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260421_001509:dir_01`
- base run id: `20260421_001009_bf16_gemm_v1_0cd407c`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `ptx_wait_commit_window_retime_without_replaying_closed_variants`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_001509`
- round loop: `round 16/100`
- hypothesis: `Round 15 kept the restored PTX microkernel on top and produced a small but real scheduler-facing nudge in the right direction: runtime improved from 24.17859173 ms to 24.17100811 ms, barrier eased from 5.48% to 5.21%, and long-scoreboard eased from 7.16% to 7.08%, while active warps stayed pinned around 16.6%. That is too small to replace the accepted base and still leaves the branch about 0.0067 ms behind the 24.16427231 ms best-known run, so the family should be treated as a flat-positive continuation rather than a closed win. The best next move is therefore one more bounded PTX control-path exploit on the current winner surface, explicitly avoiding the already measured B-first prologue, issue-grouping replay, A-then-B handoff refill, and pure future_tile_k hoist variants.`
- expected bottleneck: `Residual cp.async handoff and inner-loop control overhead in the active 128x128 PTX hot-band microkernel, not DRAM bandwidth saturation and not another restore-only action.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1956-2055, src/kernels/bf16_gemm_v1.cu:2038-2054, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. The family is still live and slightly positive, but another tweak must stay narrowly distinct from the already closed control-order, handoff-order, and address-hoist sub-variants.`
- metrics to re-check: `end-to-end median runtime versus the 24.178592 ms accepted base and the 24.164272 ms best-known run, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`

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
