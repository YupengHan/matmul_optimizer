# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted PTX hot-band anchor and discard the failed 256x128 probe`
- candidate id: `diagnosis_20260421_110945:dir_01`
- base run id: `20260421_110929_bf16_gemm_v1_342b1c5`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_best_measured_ptx_surface_after_failed_256x128_probe`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_110945`
- round loop: `round 2/100`
- hypothesis: `The 256x128 pivot probe achieved the intended register drop but still ran at 30.168576 ms because barrier and short-scoreboard stalls dominated. The correct next step is to restore the accepted PTX hot-band surface immediately so the loop can continue from a sane baseline instead of iterating on a +5.98 ms regression.`
- expected bottleneck: `Recovery to the known PTX plateau before any further latency-hiding or barrier experiment is attempted`
- code locations: `src/kernels/bf16_gemm_v1.cu:685 (compact 256x128-only B-fragment helper), src/kernels/bf16_gemm_v1.cu:1668 (256x128 compact accumulate call site), src/kernels/bf16_gemm_v1.cu:2130 (fixed hot-band dispatch route)`
- risk: `Low. This is a bounded recovery revert back to the accepted PTX surface, not a new optimization hypothesis.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`
- latest run id: `20260421_110929_bf16_gemm_v1_342b1c5`
- latest runtime: `30.168576 ms`
- latest NCU analysis: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `167.0` | Registers improved, but the probe still regressed overall throughput.
- `stall` `barrier` @ `256x128 steady-state handoff` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.32` | Barrier stalls became the dominant issue on the probed surface.
- `stall` `short_scoreboard` @ `256x128 shared / fragment handoff` | `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` = `6.77` | Short-scoreboard stalls rose sharply versus the accepted PTX baseline.

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

- `median_runtime_ms` `strictly_decreasing` from `30.16857624` | The current probe is materially regressed and must recover before forward search resumes.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `8.32` | Barrier stalls jumped on the failed probe and should come back down after recovery.
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `6.77` | Short-scoreboard stalls are part of the current local failure mode.

## Expected local changes

- `Route the hot band back to the accepted PTX 128x128 microkernel.`
- `Remove or park the compact 256x128 probe path from the active dispatch.`
- `Keep the recovery diff narrow enough that the next round can remeasure a clean baseline.`

## Delta vs previous run

- baseline run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- stall `long_scoreboard` | delta `-5.01` | trend `improved`
- stall `short_scoreboard` | delta `4.609999999999999` | trend `regressed`
- stall `barrier` | delta `2.8500000000000005` | trend `regressed`
- stall `mio_throttle` | delta `-2.8200000000000003` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-33.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-13.280000000000001` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-13.170000000000002` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-11.68` | trend `regressed`

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
