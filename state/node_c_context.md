# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 256x128 Pivot Hot-Band Kernel`
- candidate id: `diagnosis_20260420_220312:dir_01`
- base run id: `20260420_220130_bf16_gemm_v1_0893f2c`
- primary family id: `legacy::promote_the_existing_256x128_pivot_hot_band_kernel`
- planned action fingerprint: `538fb586502fa3b4`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_220312`
- round loop: `round 2/20`
- hypothesis: `Round 1/20 established the PTX one-k 128x128 branch as the new accepted base at 24.419329 ms, which already beats CUTLASS. That removes the pressure to keep shaving only the same control path and makes round 2/20 a better place to test the strongest orthogonal family still sitting in-tree. The hot-band PTX kernel is still the wall at 32.687232 ms with 200 registers per thread and only 16.62% active warps while launching a 60x50 grid over the first 6400 x 7680 rows. The existing 256x128 pivot family halves the pivot-band CTA count and restores an 8-warp CTA, so it is the cleanest next test of whether hot-band geometry and block-count overhead are now the limiting factor.`
- expected bottleneck: `Hot-band CTA geometry and block-count overhead on the current 128x128 PTX base, rather than a remaining local control-path bubble inside the winning branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:80-105, src/kernels/bf16_gemm_v1.cu:1581-1677, src/kernels/bf16_gemm_v1.cu:2071-2137`
- risk: `Moderate. The kernel already exists in-tree, but routing the default path onto it changes the hot-band family more materially than another PTX micro-retune and could lose if the larger CTA worsens the live set.`
- metrics to re-check: `end-to-end median runtime versus the new 24.419329 ms base, hot-band kernel name and grid size in ncu_details.csv, hot-band gpu__time_duration.sum, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, hot-band launch__registers_per_thread`

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
