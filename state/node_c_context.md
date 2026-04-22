# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Grouped Rows From 2 Back To 4 On The Compact Two-Stage PTX Ring`
- candidate id: `diagnosis_20260421_185158:dir_01`
- base run id: `20260421_185050_bf16_gemm_v1_434ded2a`
- primary family id: `launch_order::ptx_hotband_grouped_rows_tune`
- planned action fingerprint: `ptx_hotband_launch_order:grouped_rows_2->4_on_two_stage_compact_ring`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_185158`
- round loop: `round 8/20`
- hypothesis: `The grouped_rows=2 retest kept the recovered register budget but clearly reintroduced the long_scoreboard problem on the compact two-stage surface. Restoring grouped_rows to 4 should recover the better row-order reuse pattern from the earlier PTX anchor without reopening the losing round-6 split logic.`
- expected bottleneck: `Long-scoreboard pressure from the grouped_rows=2 launch order is now the most specific local bottleneck to remove.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:2020-2031`
- risk: `Low. This is a single-parameter launch-order restore on the currently healthy compact two-stage PTX surface.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`
- latest run id: `20260421_185050_bf16_gemm_v1_434ded2a`
- latest runtime: `25.461216 ms`
- latest NCU analysis: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.21` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.338` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.76` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.76` | barrier stalls are consuming 5.76% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `bounded_not_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Restore kFixedHotBandPtxGroupedRows from 2 back to 4.`
- `Leave the compact two-stage PTX ring unchanged.`
- `Re-measure whether the long_scoreboard rebound disappears without giving back the recovered register budget.`

## Delta vs previous run

- baseline run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- stall `long_scoreboard` | delta `5.9799999999999995` | trend `regressed`
- stall `mio_throttle` | delta `-1.9899999999999998` | trend `improved`
- stall `barrier` | delta `-0.96` | trend `improved`
- stall `short_scoreboard` | delta `0.33000000000000007` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-52.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-21.330000000000002` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-1.9600000000000009` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `1.4299999999999997` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.

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
