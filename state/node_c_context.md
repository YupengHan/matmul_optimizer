# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_03`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260420_222929:dir_03`
- base run id: `20260420_222846_bf16_gemm_v1_8ba4496`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `3587455924361acf`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260420_222929`
- round loop: `round 6/100`
- hypothesis: `The current loop should keep one restore-style family active instead of repeatedly tunneling on the latest PTX-local micro-tunes. The best historical grouping-window restore still measured 24.444416 ms, close enough to the accepted base to remain meaningful, and it gives the search an auditable locality fallback if both the helper-flattening and export-cleanup families stall.`
- expected bottleneck: `Inter-CTA locality and launch-order mapping on the accepted PTX surface, but explicitly as a restore fallback rather than the primary next attack.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:1957-1979, src/kernels/bf16_gemm_v1.cu:2097-2104`
- risk: `Low to medium. The family has historical evidence, but the latest fresh grouped traversal probe also makes it a weaker primary bet than the two PTX-local cleanup families.`
- metrics to re-check: `end-to-end median runtime versus the 24.177664 ms base and the historical 24.444416 ms restore run, hot-band gpu__time_duration.sum, lts__throughput.avg.pct_of_peak_sustained_elapsed, sm__warps_active.avg.pct_of_peak_sustained_active`

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
