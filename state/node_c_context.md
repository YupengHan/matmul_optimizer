# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260421_000721:dir_01`
- base run id: `20260421_000626_bf16_gemm_v1_7f84649`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `8e91e546243f09ff`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_000721`
- round loop: `round 15/100`
- hypothesis: `Round 14 restored the PTX winner after the round-13 handoff miss and confirmed that the regression was a one-variant failure rather than wider source drift: the current source now matches the best-known `489574e` kernel file exactly and runtime recovered from 24.48483181 ms back to 24.17859173 ms. That also means several families should be filtered out again for this round: the restore family is absorbed on the current source, the export-cleanup family is already baked into this PTX surface, and the A-then-B handoff variant is now a measured negative. With those filters applied, the strongest remaining live family is the active PTX control path. The branch still runs at only 16.62% active warps with non-trivial barrier and long-scoreboard cost, so one more bounded control-path exploit remains the best next move as long as it does not replay the already-tested B-first prologue, issue-grouping, or A-then-B handoff sub-variants.`
- expected bottleneck: `Residual control-path and consume-order overhead inside the active PTX hot-band microkernel after the absorbed restore/export cleanup and the rejected handoff variant are removed from consideration.`
- code locations: `src/kernels/bf16_gemm_v1.cu:718-802, src/kernels/bf16_gemm_v1.cu:1954-2053, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. The family is still the best active-branch lever, but prior sub-variants have mixed evidence, so another attempt must stay narrowly distinct from the already-closed control-order and handoff changes.`
- metrics to re-check: `end-to-end median runtime versus the 24.178592 ms accepted base and the 24.164272 ms best-known run, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers, hot-band gpu__time_duration.sum`

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
