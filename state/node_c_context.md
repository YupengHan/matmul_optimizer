# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The PTX One-K 128x128 Hot-Band Control Branch`
- candidate id: `diagnosis_20260420_215833:dir_01`
- base run id: `20260420_205720_bf16_gemm_v1_bb3fc52`
- primary family id: `legacy::reopen_the_ptx_one_k_128x128_hot_band_control_branch`
- planned action fingerprint: `ad14e3d0308af403`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_215833`
- round loop: `round 1/20`
- hypothesis: `Round 1/20 already spent the first budget unit on a bounded retune of the active one-K 128x128 copy cadence, and node_a measured that branch slightly slower at 25.381776 ms versus the 25.325055 ms accepted base. The dominant hot-band kernel still owns about 32.918752 ms of device time with 196 registers per thread, only 16.65% active warps, 47.93% tensor-pipe activity, 7.60% long-scoreboard stall, and 5.75% barrier stall. The PTX one-K control branch keeps the same grouped-row 128x128 grid and hot-band split, but swaps the inner accumulate/export control path. That makes it the cleanest orthogonal next test because a prior PTX measurement already landed at 25.379312 ms, close enough that a small control-path win could be real on this surface.`
- expected bottleneck: `Hot-band inner-loop control and export overhead in the standard one-K 128x128 path, rather than the peeled 64x384 residual rows or the 64x96 tail.`
- code locations: `src/kernels/bf16_gemm_v1.cu:796-1068, src/kernels/bf16_gemm_v1.cu:1957-2061, src/kernels/bf16_gemm_v1.cu:2071-2137`
- risk: `Moderate to high. The PTX WMMA path is correctness-sensitive, but it is already present in-tree and the implementation surface should stay small because node_c only needs to route the default hot-band launch onto the existing branch.`
- metrics to re-check: `end-to-end median runtime versus the current 25.381776 ms run and the prior PTX 25.379312 ms run, hot-band gpu__time_duration.sum, hot-band launch__registers_per_thread, hot-band sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct`

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
