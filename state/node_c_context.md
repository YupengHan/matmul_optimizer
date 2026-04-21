# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260420_233659:dir_01`
- base run id: `20260420_233546_bf16_gemm_v1_4bc0218`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `26b22d7f05ca7ff6`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_233659`
- round loop: `round 12/100`
- hypothesis: `Round 12/100 has to correct a search-surface mismatch before spending more budget on PTX-local micro retimes. The latest measured run improved only slightly to 24.17396832 ms, but its NCU details show the dominant hot-band kernel is `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel<(int)452>`, and the current launch path still dispatches that non-PTX sibling by default at `src/kernels/bf16_gemm_v1.cu:2084-2091`. That means the recent PTX control and barrier-family rounds were no longer acting on the measured hot path that produced the 24.16435242 ms best-known run. The immediate next move is therefore to restore the historically best measured PTX surface coherently: put the PTX microkernel back on the active hot-band dispatch and recover the staging / refill ordering that belonged to the winning grouped-window branch, so later PTX-local families become auditable again instead of floating against the wrong kernel.`
- expected bottleneck: `Search-surface drift between the currently measured non-PTX hot-band dispatch and the PTX microkernel surface that still owns the 24.164352 ms best-known runtime.`
- code locations: `src/kernels/bf16_gemm_v1.cu:719-775, src/kernels/bf16_gemm_v1.cu:1930-2034, src/kernels/bf16_gemm_v1.cu:2072-2091`
- risk: `Moderate. This is a restore, not a fresh exploit, but the current tree drifted beyond a pure one-line dispatch swap, so the recovery has to restore the PTX hot-band surface coherently enough to avoid mixing the PTX label with sibling-path behavior.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms best-known PTX run, Kernel Name in ncu_details.csv for the dominant hot-band launch, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`

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
