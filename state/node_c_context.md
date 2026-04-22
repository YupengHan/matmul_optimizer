# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Compact 128x128 PTX Grouped-Rows-4 Anchor After The Failed 256x128 Reopen`
- candidate id: `diagnosis_20260421_191808:dir_01`
- base run id: `20260421_191613_bf16_gemm_v1_9652b835`
- primary family id: `restore_base::ptx_two_stage_anchor_after_failed_256x128_reopen`
- planned action fingerprint: `restore_compact_128x128_ptx_dispatch_after_writer_safe_256x128_reopen_loss`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_191808`
- round loop: `round 12/20`
- hypothesis: `The latest 256x128 measurement is a full structural regression, not a local timing miss. Restoring the compact 128x128 PTX microkernel dispatch and grouped_rows=4 anchor is the shortest path back to the last known good surface before any further frontier experiment is layered on top.`
- expected bottleneck: `The immediate problem is the bad 256x128 hot-band geometry itself, which inflated shared-memory footprint and collapsed tensor throughput.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2154-2203`
- risk: `Low. This is a bounded dispatch restore back to the last measured compact anchor and does not require new synchronization logic.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, launch__occupancy_limit_registers`
- latest run id: `20260421_191613_bf16_gemm_v1_9652b835`
- latest runtime: `30.174224 ms`
- latest NCU analysis: `runs/20260421_191613_bf16_gemm_v1_9652b835/ncu_analysis.json`

## Relevant hotspots

- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `short_scoreboard` @ `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `43.902` | Tensor activity (36.77%) is low relative to available memory bandwidth, and active warps (16.66%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `36.77` | Tensor pipe activity is only 36.77% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- `occupancy_latency_hiding_issue` | severity `36.14` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `1.0` | Register pressure is limiting occupancy to 1 blocks per SM.
- `synchronization_barrier_issue` | severity `8.32` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__occupancy_limit_registers` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Switch the fixed hot-band dispatch back from the writer-safe 256x128 kernel to the compact 128x128 PTX microkernel.`
- `Keep the peeled 64x384 row band and 64x96 tail unchanged.`
- `Leave grouped_rows=4 and the accepted compact cadence intact on the recovery measurement.`

## Delta vs previous run

- baseline run id: `20260421_190652_bf16_gemm_v1_88a8acfc`
- stall `short_scoreboard` | delta `4.35` | trend `regressed`
- stall `mio_throttle` | delta `-3.16` | trend `improved`
- stall `long_scoreboard` | delta `-2.97` | trend `improved`
- stall `barrier` | delta `0.17999999999999972` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-34.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-13.340000000000003` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-13.299999999999997` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-11.620000000000001` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was regressed in the regressed bucket.

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
