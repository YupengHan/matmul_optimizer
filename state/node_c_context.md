# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Steady-state Barrier / Handoff Retime`
- candidate id: `diagnosis_20260421_075421:dir_01`
- base run id: `20260421_075335_bf16_gemm_v1_894a38d`
- primary family id: `legacy::steady_state_barrier_handoff_retime`
- planned action fingerprint: `retime_ptx_wait_group_and_future_refill_order_on_restored_anchor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_075421`
- round loop: `round 37/100`
- hypothesis: `Round 36 showed the kind of near-flat but structurally useful signal that is worth following once more on the live PTX anchor: the new control-path cleanup missed the accepted base by only 0.016528 ms, but both barrier and long-scoreboard moved in the right direction. That means the family is probably not exhausted yet; it likely needs one more scheduler-seam nudge that acts more directly on the handoff between `cp_async_wait_group_0`, `__syncthreads()`, and the future-tile refill order. The cleanest next sub-variant is to retime that steady-state seam without changing launch bounds, tile shape, grouped traversal, or export scratch shape.`
- expected bottleneck: `Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the seam between finishing the current MMA stage and refilling the reused stage buffer for the future tile.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2042-2053, src/kernels/bf16_gemm_v1.cu:2024-2043, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. This is still a bounded scheduler retime on the live hot path, but it can easily trade barrier against scoreboard without producing an end-to-end gain.`
- metrics to re-check: `end-to-end median runtime versus 24.164272 ms and 24.175471 ms, hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active`

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
