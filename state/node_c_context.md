# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Collapse The Compact PTX Wait-Sync Seam Into A Pairwise Stage Advance`
- candidate id: `diagnosis_20260421_192105:dir_01`
- base run id: `20260421_192024_bf16_gemm_v1_8fd88cb4`
- primary family id: `sync_pipeline::ptx_microkernel_wait_sync_collapse`
- planned action fingerprint: `compact_two_stage_ptx_hotband:pairwise_stage_advance_after_round12_anchor_restore`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_192105`
- round loop: `round 13/20`
- hypothesis: `The restored compact PTX loop still waits and synchronizes on every next_tile boundary before deciding whether a future refill exists. Recasting that handoff into a pairwise stage advance should reduce barrier and scoreboard pressure together without reopening the high-shared 256x128 loss surface.`
- expected bottleneck: `Barrier and long-scoreboard are the clearest remaining compact-surface bottlenecks on the restored anchor.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2092-2120`
- risk: `Moderate. This stays on the compact PTX hot loop, but it directly touches the synchronization seam that guards the async-copy pipeline.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active`
- latest run id: `20260421_192024_bf16_gemm_v1_8fd88cb4`
- latest runtime: `24.693696 ms`
- latest NCU analysis: `runs/20260421_192024_bf16_gemm_v1_8fd88cb4/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.322` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.2` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.2` | barrier stalls are consuming 8.20% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Refactor the compact PTX hot loop so wait/sync advances in pairwise stages instead of on every single next_tile boundary.`
- `Keep grouped_rows=4, 128x128 CTA geometry, and the 22,016 B shared-memory footprint unchanged.`
- `Do not mix this experiment with a tiling or export-path change.`

## Delta vs previous run

- baseline run id: `20260421_191613_bf16_gemm_v1_9652b835`
- stall `short_scoreboard` | delta `-4.359999999999999` | trend `improved`
- stall `mio_throttle` | delta `3.16` | trend `regressed`
- stall `long_scoreboard` | delta `2.98` | trend `regressed`
- stall `barrier` | delta `-0.120000000000001` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `34.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `13.400000000000006` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `13.299999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `11.82` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was improved in the improved bucket.

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
