# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_082719:dir_01`
- base run id: `20260421_075613_bf16_gemm_v1_ba8c2d7`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_from_489574ed5013268dbb79c634450d9a60155a294a`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_082719`
- round loop: `round 38/100`
- hypothesis: `Round 37 only clawed back a few microseconds from round 36 and still finished above the accepted `489574e` anchor at 24.18427181 ms versus 24.16427231 ms. The live PTX hot-band kernel remains the runtime owner, but the measured source has drifted off the best-known surface by a pair of small scheduler-path edits that did not convert into a real win. The highest-value move now is to restore the exact accepted PTX surface on the current tree, re-measure it on the current harness state, and re-open the tighter exploit families only from that clean anchor instead of stacking more tweaks on top of a regressed branch.`
- expected bottleneck: `Source drift away from the accepted PTX hot-band steady state, not DRAM saturation and not another immediate structural pivot.`
- code locations: `src/kernels/bf16_gemm_v1.cu:153-156, src/kernels/bf16_gemm_v1.cu:2000-2060, src/kernels/bf16_gemm_v1.cu:2107-2128`
- risk: `Low. The exact restore surface is already buildable and previously measured as the current accepted best, so this is primarily a search reset rather than a novel correctness risk.`
- metrics to re-check: `end-to-end median runtime versus 24.18427181 ms and the accepted 24.16427231 ms anchor, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
