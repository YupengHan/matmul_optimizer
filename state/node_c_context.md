# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Accepted Base And Increase PTX Grouped-Row Depth`
- candidate id: `diagnosis_20260421_145629_round03_5383596d:dir_01`
- base run id: `20260421_145629_bf16_gemm_v1_5383596d`
- primary family id: `launch_order::ptx_hotband_grouped_rows_tune`
- planned action fingerprint: `restore_ptx_hotband_baseline:grouped_rows_4->8`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_145629_round03_5383596d`
- round loop: `round 3/10`
- hypothesis: `The accepted PTX hot-band kernel is still the fastest measured family, but its grouped-row traversal may not be feeding B-tile reuse aggressively enough. Restoring the accepted base and increasing kFixedHotBandPtxGroupedRows from 4 to 8 should keep more adjacent row tiles on the same hot-band B tile before advancing columns, which may reduce scoreboard waste without reopening the failed 64x384 expansion.`
- expected bottleneck: `launch-order and B-tile reuse inefficiency inside the accepted PTX hot-band traversal`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:1983, src/kernels/bf16_gemm_v1.cu:1988, src/kernels/bf16_gemm_v1.cu:2114`
- risk: `Low-to-moderate risk: the change is isolated, but a larger grouped-row depth can easily help B reuse while hurting A locality.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_145629_bf16_gemm_v1_5383596d`
- latest runtime: `47.290880 ms`
- latest NCU analysis: `runs/20260421_145629_bf16_gemm_v1_5383596d/ncu_analysis.json`

## Relevant hotspots

- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.33` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.67` | Active warps are only 16.67% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.214` | Tensor activity (48.45%) is low relative to available memory bandwidth, and active warps (16.67%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.45` | Tensor pipe activity is only 48.45% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.67` | Active warps are only 16.67% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.98` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.98` | barrier stalls are consuming 5.98% of active warp issue slots.

## Guardrail metrics

- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `lts__throughput.avg.pct_of_peak_sustained_elapsed` `non_decreasing` from `N/A` | N/A

## Expected local changes

- `Restore the accepted PTX hot-band baseline by undoing the round-2 pivot-row rebalance.`
- `Increase kFixedHotBandPtxGroupedRows from 4 to 8 while keeping the default PTX hot-band launch and 64x96 tail intact.`

## Delta vs previous run

- baseline run id: `20260421_142317_bf16_gemm_v1_5ea07e35`
- stall `barrier` | delta `-4.109999999999999` | trend `improved`
- stall `long_scoreboard` | delta `1.3099999999999996` | trend `regressed`
- stall `mio_throttle` | delta `-1.13` | trend `improved`
- stall `short_scoreboard` | delta `-0.4500000000000002` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-14.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `8.729999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `6.109999999999999` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `5.68` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was improved in the improved bucket.

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
