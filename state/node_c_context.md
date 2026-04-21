# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260420_222244:dir_01`
- base run id: `20260420_221336_bf16_gemm_v1_8eb3db3`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `df8f5978fe0c5afd`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_222244`
- round loop: `round 5/20`
- hypothesis: `The grouped-CTA traversal retune just lost 0.341504 ms versus the 24.177664 ms accepted PTX base, which is a strong signal that CTA ordering is not the next high-leverage knob on this branch. The active kernel is still the PTX 128x128 hot-band microkernel at 200 registers per thread with only 16.60% active warps and 48.36% tensor-pipe activity, while DRAM remains low at 9.73%. The next best move is therefore to stay on the winning PTX branch and retune the inner control/export surface that actually governs issue efficiency: copy/consume order, helper lifetime, and export sequencing inside the live microkernel, not another grid-traversal experiment.`
- expected bottleneck: `Residual PTX hot-band control-path overhead and live-range pressure inside the current 128x128 microkernel, not global bandwidth or another CTA-ordering miss.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-860, src/kernels/bf16_gemm_v1.cu:1010-1075, src/kernels/bf16_gemm_v1.cu:1957-2061`
- risk: `Moderate. This stays on the best measured family and touches the actual hot path, but PTX control-surface tweaks can still collapse into noise or silently grow live ranges if the scope is not bounded.`
- metrics to re-check: `end-to-end median runtime versus the 24.177664 ms base, hot-band gpu__time_duration.sum, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
