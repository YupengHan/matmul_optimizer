# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Steady-state Barrier / Handoff Retime`
- candidate id: `diagnosis_20260420_235953:dir_01`
- base run id: `20260420_235922_bf16_gemm_v1_489574e`
- primary family id: `legacy::steady_state_barrier_handoff_retime`
- planned action fingerprint: `8f8b5eca1122e2da`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_235953`
- round loop: `round 13/100`
- hypothesis: `Round 12 repaired the search-surface mismatch and restored the PTX microkernel as the dominant hot-band launch. The new best run at 24.16427231 ms slightly improved the exact scheduler-facing counters that still matter on this branch: active warps rose to 16.63%, barrier eased to 5.43%, and long-scoreboard eased to 7.17%, while DRAM stayed low at 12.44%. A source diff against `df5bac2` is now comment-only, so the restore and export-cleanup families are absorbed again and should be filtered out. The highest-value unabsorbed follow-on on the active PTX surface is therefore the narrow handoff seam around `cp_async_wait_group_0`, `__syncthreads()`, and the future-tile refill order. The prior barrier/handoff attempt should not be treated as negative evidence here because it was measured on the non-PTX sibling dispatch, not on the restored PTX microkernel that now owns the runtime.`
- expected bottleneck: `Residual wait-group and barrier cadence in the active PTX hot-band steady-state loop, especially the handoff between MMA issue completion and future-tile refill.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2008-2022, src/kernels/bf16_gemm_v1.cu:2024-2053, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. The family is bounded and now truly acts on the live PTX surface, but it still trades scheduler timing at the margin and can easily reshape barrier versus scoreboard without producing a measurable end-to-end win.`
- metrics to re-check: `end-to-end median runtime versus the 24.164272 ms current best run, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`

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
