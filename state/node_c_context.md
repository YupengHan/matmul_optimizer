# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Microkernel Barriers On The Restored 128x128 Anchor`
- candidate id: `diagnosis_20260421_073952:dir_01`
- base run id: `20260421_014255_bf16_gemm_v1_a16425e`
- primary family id: `aggressive::trim_microkernel_barriers_without_x32_shared_blowup`
- planned action fingerprint: `trim_ptx_wait_sync_cadence_on_restored_anchor_without_two_k_stage_buffers`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_073952`
- round loop: `round 34/100`
- hypothesis: `The loop is back on the exact PTX anchor, and the last two occupancy probes already answered the register-only question: both the PTX and non-PTX 128x128 launch-bounds variants cut registers to about 168 and raised active warps to roughly 24.7%, but both still regressed because synchronization cost spiked into the ~11% band. The accepted anchor keeps the hot-band kernel at 22.016 KB shared memory per block, 200 registers per thread, 16.63% active warps, 7.23% long-scoreboard stall, and 5.49% barrier stall. The next coherent move is therefore to keep the restored 128x128 PTX surface intact and surgically trim the wait/sync cadence or export handoff inside the PTX microkernel, without reintroducing the larger x32 shared-memory footprint.`
- expected bottleneck: `Barrier cadence and PTX export/control handoff inside the single-K 128x128 PTX hot-band microkernel, now that recovery is complete and the failed residency probes isolated synchronization as the limiting tax on higher occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1832-2060`
- risk: `High. This is microkernel-level control-flow surgery on the best-known branch, so correctness and codegen stability are both fragile.`
- metrics to re-check: `end-to-end median runtime versus 24.171008 ms, hot-band gpu__time_duration.sum, hot-band launch__shared_mem_per_block_allocated, hot-band launch__registers_per_thread, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, hot-band sm__warps_active.avg.pct_of_peak_sustained_active`

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
