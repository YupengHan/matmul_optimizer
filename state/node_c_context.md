# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Increase PTX Grouped-Row Depth On The Clean Baseline`
- candidate id: `diagnosis_20260421_150626_round01_clean_6cc462c4:dir_01`
- base run id: `20260421_150626_bf16_gemm_v1_6cc462c4`
- primary family id: `launch_order::ptx_hotband_grouped_rows_tune`
- planned action fingerprint: `clean_ptx_hotband_baseline:grouped_rows_4->8`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_150626_round01_clean_6cc462c4`
- round loop: `round 1/10`
- hypothesis: `The accepted PTX hot-band baseline may still be wasting issue slots because each hot-band B tile is only reused across four adjacent row tiles before the traversal advances columns. Increasing kFixedHotBandPtxGroupedRows from 4 to 8 should keep each B tile live across more rows, potentially reducing scoreboard pressure without changing the row split or K-stage structure.`
- expected bottleneck: `launch-order and B-tile reuse inefficiency inside the accepted PTX hot-band traversal`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:1983, src/kernels/bf16_gemm_v1.cu:1988, src/kernels/bf16_gemm_v1.cu:2114`
- risk: `Low-to-moderate risk: the edit is isolated, but deeper row grouping can help B reuse while hurting A locality or cache balance.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, lts__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_150626_bf16_gemm_v1_6cc462c4`
- latest runtime: `24.323521 ms`
- latest NCU analysis: `runs/20260421_150626_bf16_gemm_v1_6cc462c4/ncu_analysis.json`

## Relevant hotspots

- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.78` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.334` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.46` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.46` | barrier stalls are consuming 5.46% of active warp issue slots.

## Guardrail metrics

- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `lts__throughput.avg.pct_of_peak_sustained_elapsed` `non_decreasing` from `N/A` | N/A

## Expected local changes

- `Keep the accepted PTX hot-band row split and default launch intact.`
- `Increase kFixedHotBandPtxGroupedRows from 4 to 8 and remeasure on the same fixed benchmark.`

## Delta vs previous run

- baseline run id: `20260421_150200_bf16_gemm_v1_f4fa1bbe`
- stall `barrier` | delta `-0.45999999999999996` | trend `improved`
- stall `long_scoreboard` | delta `0.35000000000000053` | trend `regressed`
- stall `mio_throttle` | delta `-0.25` | trend `improved`
- stall `short_scoreboard` | delta `-0.09999999999999964` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `2.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.6800000000000015` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `1.3000000000000007` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.04999999999999716` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.

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
