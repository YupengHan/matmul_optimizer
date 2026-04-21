# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore accepted grouped_rows=8 hot-band consumer ordering`
- candidate id: `diagnosis_20260421_002857:dir_01`
- base run id: `20260421_002817_bf16_gemm_v1_a471728`
- primary family id: `legacy::restore_accepted_grouped_rows_8_hot_band_consumer_ordering`
- planned action fingerprint: `restore_grouped_rows_8_ptx_consumer_ordering_surface`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_002857`
- round loop: `round 18/100`
- hypothesis: `Round 17 restored the PTX winner surface and pulled runtime back from 24.19086361 ms to 24.17296028 ms, with counters returning close to the prior PTX band: active warps rebounded to 16.63%, long-scoreboard tightened to 7.13%, and tensor activity rose to 48.41%. That means the restore family is absorbed again and the loop should stop spending rounds on re-anchoring. The best next move is now the strongest alternate PTX family kept alive from round_history: the grouped_rows=8 consumer-ordering surface. It preserves the PTX hot-band microkernel while materially changing CTA grouping and consumer locality, which makes it the cleanest next attempt to move beyond the current 24.17 plateau without reopening the already mixed control-path family first.`
- expected bottleneck: `Grouped-row traversal and consumer-order locality on the PTX hot-band microkernel, not the already-restored prologue/refill seam on the grouped_rows=4 winner surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:1979-1993, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Moderate. This is an alternate PTX surface rather than the current default, but it is still the highest-confidence live family once restore is absorbed again.`
- metrics to re-check: `end-to-end median runtime versus the 24.172960 ms restored run and the 24.164272 ms best-known run, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed, correctness pass rate across all 3 cases`

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
