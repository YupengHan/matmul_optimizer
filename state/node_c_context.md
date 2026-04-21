# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage`
- candidate id: `diagnosis_20260420_232331:dir_01`
- base run id: `20260420_232254_bf16_gemm_v1_78421da`
- primary family id: `legacy::trim_the_grouped_row_128x128_sibling_export_scratch_to_the_ptx_style_single_stage`
- planned action fingerprint: `739689f47db8e67a`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_232331`
- round loop: `round 10/100`
- hypothesis: `Round 9 turned the grouped-row non-PTX 128x128 sibling from a historical escape hatch into a directly measured live branch: switching the default hot-band dispatch onto that sibling measured 24.18073654 ms, which is only 0.00008011 ms slower than the accepted-base run at 24.18065643 ms and therefore effectively PASS_FLAT on the active search anchor. The NCU headline signature also stayed in the same band instead of collapsing: active warps held at 16.62, long-scoreboard stayed at 7.26, and barrier only moved to 5.48. That means the branch validation step is done. The cleanest next move is the historically positive follow-on inside that family: replace the sibling's heavier generic export scratch lifetime with the PTX-style single-stage per-warp scratch path that previously improved the sibling branch from 24.449024 ms to 24.422464 ms. Now that the sibling route is live in the current tree, this bounded export-side trim is the highest-upside next step without reopening a broader family pivot.`
- expected bottleneck: `Shared export and writeback overhead inside the grouped-row non-PTX 128x128 sibling, especially the sibling branch's heavier export scratch lifetime after the hot-band dispatch has already moved onto that family.`
- code locations: `src/kernels/bf16_gemm_v1.cu:110-137, src/kernels/bf16_gemm_v1.cu:936-1068, src/kernels/bf16_gemm_v1.cu:1843-1948`
- risk: `Medium. The family is bounded and historically positive, but it still leaves the absolute best-known PTX run behind unless the sibling export trim converts the newly validated flat branch into a real win.`
- metrics to re-check: `end-to-end median runtime versus the 24.164352 ms best-known PTX run, end-to-end median runtime versus the 24.180656 ms accepted-base run, hot-band gpu__time_duration.sum, shared-memory footprint or allocation on the sibling path, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, correctness pass rate across all 3 cases`

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
