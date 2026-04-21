# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Accepted Grouped-Rows-8 Hot-Band Consumer Ordering`
- candidate id: `diagnosis_20260421_012002:dir_01`
- base run id: `20260421_011816_bf16_gemm_v1_20cad79`
- primary family id: `legacy::restore_accepted_grouped_rows_8_hot_band_consumer_ordering`
- planned action fingerprint: `restore_grouped_rows_8_ptx_consumer_ordering_surface`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_012002`
- round loop: `round 28/100`
- hypothesis: `The exact PTX restore and the non-PTX sibling have now both been remeasured on fresh rounds and both landed back in the same plateau regime. That means round 28 should stop spending budget on those two anchors alone and instead use the restored PTX winner to evaluate the last materially different PTX grouping surface that is still sitting in the frontier: grouped_rows=8 consumer ordering. This branch already has one older loss, but it changes CTA grouping and consumer locality more materially than another frozen micro-retime. Running it once from the clean anchor is the fastest way to decide whether it deserves to stay in the live queue at all.`
- expected bottleneck: `Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the already-replayed exact PTX restore and not another same-plateau alternate-surface A/B.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:1956-2060, src/kernels/bf16_gemm_v1.cu:1983-1993`
- risk: `Medium. This family already has one measured loss, so the main risk is spending a round to confirm that the alternate grouping surface is still inferior. That confirmation is still useful because it would let the loop close this branch with current evidence instead of leaving it half-open in the frontier.`
- metrics to re-check: `end-to-end median runtime, correctness pass rate across all 3 cases, hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
