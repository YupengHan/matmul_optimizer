# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Active PTX One-K 128x128 Hot-Band Control Path`
- candidate id: `diagnosis_20260420_220747:dir_01`
- base run id: `20260420_220628_bf16_gemm_v1_676f10d`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `2ad5f5278d8d4a4c`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_220747`
- round loop: `round 3/20`
- hypothesis: `Round 2/20 falsified the 256x128 geometry pivot hard: end-to-end runtime regressed from the accepted 24.419329 ms PTX base to 30.286848 ms, and the hot-band kernel alone grew to 43.291456 ms even though registers fell to 168/thread. That means the best next move is not another wide family jump but a bounded exploit pass on top of the accepted PTX one-k 128x128 branch. The winning PTX base still had 200 registers per thread, only 16.62% active warps, 7.20% long-scoreboard stall, and 5.41% barrier stall, so there is still room to trim local control/export overhead without repeating the failed geometry experiment.`
- expected bottleneck: `Residual control-path overhead and live-range pressure inside the accepted PTX one-k 128x128 hot-band branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-1068, src/kernels/bf16_gemm_v1.cu:1957-2061, src/kernels/bf16_gemm_v1.cu:2071-2137`
- risk: `Moderate. PTX microkernel changes are correctness-sensitive, but this stays on the last measured winner instead of introducing another new geometry family.`
- metrics to re-check: `end-to-end median runtime versus the accepted 24.419329 ms PTX base, hot-band gpu__time_duration.sum, hot-band launch__registers_per_thread, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
