# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_02`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260420_232331:dir_02`
- base run id: `20260420_232254_bf16_gemm_v1_78421da`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `8e91e546243f09ff`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260420_232331`
- round loop: `round 10/100`
- hypothesis: `The active PTX branch still owns the best-known custom runtime at 24.16435242 ms, so it cannot be dropped from the queue just because the last two PTX-local tweaks flattened out. The right interpretation of rounds 7 through 9 is narrower: the export-address cleanup harvested a tiny writeback win, the follow-up issue-grouping retime flattened, and the sibling dispatch pivot then validated an off-branch alternative without beating the PTX best. That leaves one coherent PTX fallback alive: a bounded control-path exploit that stays on the best-known PTX surface but avoids simply replaying the same export cleanup or handoff micro-change. If the sibling export trim fails to convert its flat branch into a win, this remains the strongest on-surface family to revisit.`
- expected bottleneck: `Residual PTX hot-band control-path overhead on the best-known 128x128 PTX surface, especially helper lifetime and consume-order friction that the export-address cleanup did not remove.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-860, src/kernels/bf16_gemm_v1.cu:1010-1075, src/kernels/bf16_gemm_v1.cu:1957-2061`
- risk: `Moderate. The family has one historical PASS_WIN and multiple later PASS_FLAT outcomes, so another attempt must be materially different from the already-baked control-order tweaks or it will likely collapse back into noise.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms best-known PTX run, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band gpu__time_duration.sum`

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
