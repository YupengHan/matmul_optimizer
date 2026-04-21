# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 256x128 Pivot Hot-Band Kernel`
- candidate id: `diagnosis_20260421_003535:dir_01`
- base run id: `20260421_003431_bf16_gemm_v1_f198bbb`
- primary family id: `legacy::promote_the_existing_256x128_pivot_hot_band_kernel`
- planned action fingerprint: `promote_existing_256x128_pivot_hot_band_dispatch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_003535`
- round loop: `round 20/100`
- hypothesis: `The current PTX winner surface still sits at only about 48% tensor-pipe activity, 47.8% SM throughput, and 16.6% active warps. Under the new human guidance, that means the next recommendation should not be another narrow PTX-local retime whose upside is measured in hundredths of a millisecond. The strongest aggressive live family is to promote the existing 256x128 pivot hot-band kernel and give the hot region a materially different reuse geometry. That branch is the cleanest in-tree candidate for recovering multi-millisecond headroom because it changes the hot-band shape, staging footprint, and control amortization all at once rather than chasing another tiny local ordering tweak.`
- expected bottleneck: `Structural latency hiding and control amortization on the hot band due to undersized effective work per scheduling decision, not just one more PTX microkernel handoff seam.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1580-1670, src/kernels/bf16_gemm_v1.cu:2108-2128, src/kernels/bf16_gemm_v1.cu:2130-2135`
- risk: `Medium to high. This is a broad hot-band dispatch change, but that is now a feature rather than a bug because the user explicitly wants more aggressive implementations once a family is chosen.`
- metrics to re-check: `end-to-end median runtime versus the 24.171520 ms restored PTX run, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__throughput.avg.pct_of_peak_sustained_elapsed, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, hot-band gpu__time_duration.sum`

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
