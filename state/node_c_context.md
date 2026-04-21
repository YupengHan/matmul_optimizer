# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling`
- candidate id: `diagnosis_20260420_225317:dir_01`
- base run id: `20260420_225251_bf16_gemm_v1_306839d`
- primary family id: `legacy::port_grouped_row_traversal_into_the_non_ptx_128x128_sibling`
- planned action fingerprint: `50dacc5cc17f8c60`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_225317`
- round loop: `round 9/100`
- hypothesis: `Rounds 7 and 8 on the restored grouped-rows-4 PTX surface produced the clearest saturation signal yet for the active PTX-local micro families. The export-address cleanup established a new best custom at 24.164352 ms, but only by 0.016304 ms and still as PASS_FLAT; the follow-up control-path issue-grouping tweak then regressed slightly to 24.170400 ms, again as PASS_FLAT. Across both runs the signature barely moved: active warps stayed pinned at 16.61-16.62, barrier stayed in the 5.42-5.45 band, and long-scoreboard stayed in the 7.24-7.26 band. That is enough evidence to stop spending the next round on another tiny PTX-local retime. The best next family is to preserve grouped-row locality but pivot off the active PTX microkernel onto the non-PTX 128x128 sibling, which historically stayed reasonably close to the best PTX surface while materially changing the hot-band control/export path.`
- expected bottleneck: `The active PTX control/export surface looks saturated; the next opportunity is preserving grouped-row locality while changing the hot-band control/export implementation family away from the PTX microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:1843-1948, src/kernels/bf16_gemm_v1.cu:2091-2139`
- risk: `Medium. This changes the dominant hot-band family rather than another micro-tweak, but it still stays inside the existing grouped-row 128x128 geometry instead of reopening the more disruptive 256x128 or full-band families.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms best-known PTX run, correctness pass rate across all 3 cases, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band gpu__time_duration.sum`

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
