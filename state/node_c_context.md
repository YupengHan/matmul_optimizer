# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune Hot-Band CTA Traversal On The 128x128 PTX Grid`
- candidate id: `diagnosis_20260420_221111:dir_01`
- base run id: `20260420_221009_bf16_gemm_v1_68c21ac`
- primary family id: `legacy::retune_hot_band_grouped_cta_traversal_on_the_128x128_grid`
- planned action fingerprint: `cb77d05553cb3c86`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_221111`
- round loop: `round 4/20`
- hypothesis: `Round 3/20 recovered from the 256x128 loss and set a new best at 24.177664 ms, but the hot-band PTX kernel's NCU signature barely moved relative to the previous PTX base: kernel time remained about 32.687 ms and register count stayed at 200/thread. That suggests the unroll tweak was only a small perturbation rather than a structural feed breakthrough. The best next move is therefore a cheap orthogonal traversal/locality test on the proven PTX base. The current branch still launches a 60x50 hot-band grid while only two 4-warp CTAs can stay resident per SM, so a grouped-row or serpentine traversal remap is the best low-risk probe of inter-CTA locality.`
- expected bottleneck: `Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid under low occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:149-157, src/kernels/bf16_gemm_v1.cu:1981-1997, src/kernels/bf16_gemm_v1.cu:2071-2137`
- risk: `Low to moderate. The surface is small and reversible, but previous CTA-order experiments have had mixed evidence, so the upside is bounded.`
- metrics to re-check: `end-to-end median runtime versus the 24.177664 ms base, hot-band gpu__time_duration.sum, hot-band lts__throughput.avg.pct_of_peak_sustained_elapsed, hot-band dram__throughput.avg.pct_of_peak_sustained_elapsed, hot-band sm__warps_active.avg.pct_of_peak_sustained_active`

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
