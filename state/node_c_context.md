# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Apply Only A Minimal PTX Export Address Cleanup`
- candidate id: `diagnosis_20260420_223553:dir_01`
- base run id: `20260420_223530_bf16_gemm_v1_82c8e60`
- primary family id: `legacy::apply_only_a_minimal_ptx_export_address_cleanup`
- planned action fingerprint: `0a4f037bb055c349`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_223553`
- round loop: `round 7/100`
- hypothesis: `Round 6 recovered the accepted PTX grouping surface and produced a clear runtime win, but the restored profile still carries the same occupancy ceiling and modest barrier / scoreboard costs. That points to the remaining overhead sitting close to the PTX export path rather than in another dispatch or locality knob. The best bounded next move is therefore to keep the restored grouping window intact and simplify only the PTX export address/control surface so writeback bookkeeping dies sooner without changing the MMA loop or widening the hot path.`
- expected bottleneck: `PTX export-side address/control overhead and scratch bookkeeping on the restored accepted hot-band surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:925-947, src/kernels/bf16_gemm_v1.cu:1008-1065, src/kernels/bf16_gemm_v1.cu:2044-2047`
- risk: `Low to medium. This keeps the freshly restored PTX branch intact and only narrows the export surface, but the upside is bounded and it can still become a no-op if the compiler already simplified the current path.`
- metrics to re-check: `end-to-end median runtime versus the 24.180656 ms restored base, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__registers_per_thread, hot-band gpu__time_duration.sum`

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
