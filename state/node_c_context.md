# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Steady-state Barrier / Handoff Retime`
- candidate id: `diagnosis_20260420_233235:dir_01`
- base run id: `20260420_233034_bf16_gemm_v1_11df0f1`
- primary family id: `legacy::steady_state_barrier_handoff_retime`
- planned action fingerprint: `8f8b5eca1122e2da`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_233235`
- round loop: `round 11/100`
- hypothesis: `Round 10 forced an explicit audit of which queued families are still actionable versus already absorbed in the current source. After filtering out the sibling export-trim no-op and then measuring a real PTX control-path fallback, the latest run still regressed to 24.19046402 ms while the headline signature barely moved: active warps stayed at 16.61, barrier stayed at 5.46, and long-scoreboard stayed at 7.24. That combination means neither another export-side replay nor another trivial prologue-order nudge is the next best bet. The cleanest remaining unabsorbed lever on the current PTX winner is a narrower retime of the steady-state wait-group and handoff cadence around `cp.async`, `__syncthreads()`, and the future-tile refill path. It keeps the accepted PTX surface intact while attacking the scheduler seam that is still visibly exposed after the export cleanup and the latest control-path tweak.`
- expected bottleneck: `Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the handoff between the current stage's MMA issue and the future-tile refill sequence.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1998-2017, src/kernels/bf16_gemm_v1.cu:2015-2027, src/kernels/bf16_gemm_v1.cu:2032-2033`
- risk: `Moderate. The family is bounded and still unabsorbed, but the current source already contains the strongest obvious one-sync cleanup, so another retime can easily reshuffle barrier versus scoreboard without creating a real runtime win.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms best-known PTX run, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`

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
