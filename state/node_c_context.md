# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune PTX Hot-Band Grouped Rows From 4 Down To 2 On The 3-Stage Surface`
- candidate id: `diagnosis_20260421_183411:dir_01`
- base run id: `20260421_183233_bf16_gemm_v1_4948b8ea`
- primary family id: `launch_order::ptx_hotband_grouped_rows_tune`
- planned action fingerprint: `ptx_hotband_launch_order:grouped_rows_4->2_on_3stage_pg2s`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_183411`
- round loop: `round 5/20`
- hypothesis: `The current 3-stage run already removed long_scoreboard as the dominant tax, so the remaining regression is mostly handoff depth: barrier is up by 1.25 pts and mio_throttle is up by 0.59 while active warps stay flat. Reducing PTX grouped rows from 4 to 2 is the smallest way to shorten CTA group depth and reduce synchronization pressure without giving back the 3-stage latency-hiding benefit or touching the active PTX dispatch.`
- expected bottleneck: `Grouped-row batching is likely over-amortizing locality on the 3-stage surface and paying extra barrier plus handoff delay per CTA group.`
- code locations: `src/kernels/bf16_gemm_v1.cu:155-156, src/kernels/bf16_gemm_v1.cu:2017-2024`
- risk: `Low-moderate. This is a one-constant launch-order retune on the current winning kernel body, but smaller CTA groups can still lose locality if the batching cut is too aggressive.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_183233_bf16_gemm_v1_4948b8ea`
- latest runtime: `25.251841 ms`
- latest NCU analysis: `runs/20260421_183233_bf16_gemm_v1_4948b8ea/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `mio_throttle` @ `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.2` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.62` | Tensor activity (48.10%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.1` | Tensor pipe activity is only 48.10% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- `synchronization_barrier_issue` | severity `7.6` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `7.6` | barrier stalls are consuming 7.60% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `bounded_not_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Retune kFixedHotBandPtxGroupedRows from 4 to 2.`
- `Leave the 3-stage PTX ring intact.`
- `Do not touch launch bounds, stage count, or the accumulator schedule in the first pass.`

## Delta vs previous run

- baseline run id: `20260421_182631_bf16_gemm_v1_1f02b147`
- stall `long_scoreboard` | delta `-5.23` | trend `improved`
- stall `barrier` | delta `1.25` | trend `regressed`
- stall `mio_throttle` | delta `0.5900000000000003` | trend `regressed`
- stall `short_scoreboard` | delta `0.039999999999999813` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-5.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.5199999999999996` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-0.3200000000000003` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.29999999999999716` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.

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
