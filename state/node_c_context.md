# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Deepen The Active PTX Hot-Band To A 3-Stage Pg2s Pipeline`
- candidate id: `diagnosis_20260421_182858:dir_01`
- base run id: `20260421_182631_bf16_gemm_v1_1f02b147`
- primary family id: `async_copy::ptx_hotband_three_stage_pg2s`
- planned action fingerprint: `extend_ptx_128x128_pipeline_to_three_stage_pg2s_without_register_budget_growth`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_182858`
- round loop: `round 4/20`
- hypothesis: `After restoring launch_bounds to 2, the PTX anchor regained low barrier and low short-scoreboard, but the remaining gap is now long_scoreboard plus mio_throttle at only 16.60% active warps. A 3-stage Pg2s ring should hide more global-to-shared latency by keeping one extra refill in flight, so the kernel can recover tensor activity without needing the failed register-interleave rewrite.`
- expected bottleneck: `Global-to-shared latency hiding at low occupancy: long_scoreboard 5.45% and mio_throttle 3.98% indicate cp.async completion is still arriving too late for the current two-stage PTX pipeline.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1999-2004, src/kernels/bf16_gemm_v1.cu:2042-2056, src/kernels/bf16_gemm_v1.cu:2076-2088`
- risk: `Moderate-high. This touches the PTX prolog, the steady-state refill order, and the drain sequencing together, and it can easily grow shared memory or destabilize wait_group ordering if done sloppily.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, dram__throughput.avg.pct_of_peak_sustained_elapsed, launch__shared_mem_per_block_allocated`
- latest run id: `20260421_182631_bf16_gemm_v1_1f02b147`
- latest runtime: `25.063408 ms`
- latest NCU analysis: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `mio_throttle` @ `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.2` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.33` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.35` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.35` | barrier stalls are consuming 6.35% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `bounded_growth_only` from `N/A` | N/A

## Expected local changes

- `Expand the PTX a_shared and b_shared ring from two stages to three.`
- `Retune the PTX prolog and steady-state wait_group ordering to keep an extra refill in flight.`
- `Leave the active PTX dispatch and grouped_rows constant unchanged in the first pipeline-depth probe.`

## Delta vs previous run

- baseline run id: `20260421_182124_bf16_gemm_v1_49dfa799`
- stall `short_scoreboard` | delta `-5.46` | trend `improved`
- stall `barrier` | delta `-3.380000000000001` | trend `improved`
- stall `long_scoreboard` | delta `3.2800000000000002` | trend `regressed`
- stall `mio_throttle` | delta `2.59` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `34.0` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Theoretical Occupancy` | delta `-8.329999999999998` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-8.14` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-1.6099999999999994` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was regressed in the regressed bucket.

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
