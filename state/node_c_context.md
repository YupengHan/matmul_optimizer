# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The Auxiliary 256x128 Hot-Band Schedule As The Next Structural Probe`
- candidate id: `diagnosis_20260421_010737:dir_01`
- base run id: `20260421_010424_bf16_gemm_v1_f6d1219`
- primary family id: `legacy::retune_the_auxiliary_256x128_hot_band_k_loop_schedule`
- planned action fingerprint: `rehydrate_auxiliary_256x128_schedule_surface_from_9a4bb85409600456179030fc1eb1e59eb5ea3722`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_010737`
- round loop: `round 25/100`
- hypothesis: `The restored PTX winner is correct again, but it is still trapped in the same plateau signature that now defines the whole 24.16-24.19 ms cluster: tensor activity is only 48.39%, achieved warps are only 16.62%, DRAM is just 12.48%, and occupancy is still register-limited. That means round 25 should explicitly stop prioritizing another frozen PTX micro-retime and instead spend budget on the cleanest remaining structural family. The half-panel branch already consumed its grace budget and stays closed on correctness. The direct 256x128 pivot family is also closed-negative. The remaining bounded geometry-side branch is the auxiliary 256x128 schedule family: it changes hot-band control amortization and reuse shape without reopening the broken half-panel export path. Node C should therefore treat this as a real family re-entry rather than a timid one-line replay and use the recovered 256x128 surface as the base for an aggressive within-family implementation.`
- expected bottleneck: `Hot-band CTA geometry, control amortization, and latency hiding on the wide 256x128 schedule family, not another PTX-local barrier or scoreboard seam on the already plateaued 128x128 winner surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1580-1676, src/kernels/bf16_gemm_v1.cu:2070-2138, src/kernels/bf16_gemm_v1.cu:150-156`
- risk: `Medium to high. Historical support for this family is materially weaker than the PTX winner, and a too-broad dispatch swap can replay the closed 256x128 regression. It remains the best live structural probe only because the higher-ceiling half-panel family is now decisively closed on correctness.`
- metrics to re-check: `end-to-end median runtime, correctness pass rate across all 3 cases, hot-band gpu__time_duration.sum, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
