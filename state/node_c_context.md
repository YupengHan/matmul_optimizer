# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Continue The Active PTX One-K 128x128 Control-Path Exploit`
- candidate id: `diagnosis_20260421_082126:dir_01`
- base run id: `20260421_081904_bf16_gemm_v1_d327dee`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `ptx_wait_commit_window_retime_without_replaying_closed_variants`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_082126`
- round loop: `round 39/100`
- hypothesis: `Round 38 restored the exact accepted PTX surface and improved the runtime back to 24.17151993 ms, but it still finished about 0.007 ms behind the accepted best. That puts the loop back on the correct anchor and reopens the tight PTX exploit family that already showed the cleanest near-best evidence: retiming the initial wait/commit window on the same 128x128 PTX microkernel. Because the restore did not fully recover the best measurement, the next budget unit should be spent on this bounded reopen rather than immediately restoring again.`
- expected bottleneck: `Residual cp.async wait-group timing and control-path latency in the PTX 128x128 hot-band microkernel after the exact restore surface has been re-established.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2008-2022, src/kernels/bf16_gemm_v1.cu:2042-2054, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. This family stays on the dominant PTX surface and historically built cleanly, but its upside is measured in hundredths of a millisecond and it is easy to replay a closed negative variant if the change grows beyond one bounded wait/commit-window retime.`
- metrics to re-check: `end-to-end median runtime versus 24.17151993 ms and the accepted 24.16427231 ms anchor, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
