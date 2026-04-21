# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260421_075055:dir_01`
- base run id: `20260421_074828_bf16_gemm_v1_f07f873`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `retune_active_ptx_one_k_control_export_path_on_restored_anchor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_075055`
- round loop: `round 36/100`
- hypothesis: `The current source is back on the accepted PTX anchor, and the recovery measurement reconfirms the same structural signature: the hot-band PTX kernel still dominates runtime at roughly the same end-to-end cost, active warps remain pinned near 16.62%, registers stay occupancy-limited at 2 CTAs, and long-scoreboard remains elevated at 7.17%. Round 34 ruled out one specific export-scratch trimming idea, but it did not invalidate the whole active-PTX family. The best next move is therefore a bounded control-path exploit on the restored one-K PTX branch that avoids replaying the failed pair-scratch export batching and instead targets remaining consume-order, export-address, or live-range friction on the hot path.`
- expected bottleneck: `Residual PTX hot-band control-path overhead and live-range pressure on the accepted one-K 128x128 branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:718-802, src/kernels/bf16_gemm_v1.cu:1955-2060, src/kernels/bf16_gemm_v1.cu:2090-2137`
- risk: `Moderate. This stays on the winning family and acts on the live hot path, but PTX control-path edits are still correctness-sensitive and can easily reshuffle stalls without creating a real runtime win.`
- metrics to re-check: `end-to-end median runtime versus 24.164272 ms and 24.175471 ms, hot-band gpu__time_duration.sum, hot-band launch__registers_per_thread, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
