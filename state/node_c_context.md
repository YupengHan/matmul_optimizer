# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop`
- candidate id: `diagnosis_20260421_093739:dir_01`
- base run id: `20260421_084952_bf16_gemm_v1_8b1af08`
- primary family id: `exploit::hoist_hot_band_shared_offsets_out_of_128x128_steady_state_loops`
- planned action fingerprint: `hoist_128x128_hot_band_warp_local_shared_offsets_out_of_steady_state_loops`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_093739`
- round loop: `single-run`
- hypothesis: `Both active 128x128 hot-band kernels recompute warp-local A-row and B-column shared offsets inside the K steady-state loop even though those offsets are invariant for the entire CTA. Hoisting those offsets once per warp should shave integer address work and reduce control dilution on a path where tensor activity is only 48.37 percent while DRAM is far from saturated.`
- expected bottleneck: `Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are stealing issue slots from tensor work.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1775-1796, src/kernels/bf16_gemm_v1.cu:1910-1925, src/kernels/bf16_gemm_v1.cu:2024-2040`
- risk: `Low. The change is local, preserves the same tile geometry, and only hoists invariant offset math.`
- metrics to re-check: `end-to-end median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active`

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
