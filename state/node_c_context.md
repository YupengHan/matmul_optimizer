# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Clean Compact PTX Launch Bounds To Target Three-CTA Residency`
- candidate id: `diagnosis_20260421_194601:dir_01`
- base run id: `20260421_194414_bf16_gemm_v1_ac1299d7`
- primary family id: `register_pressure::retune_ptx_launch_bounds`
- planned action fingerprint: `clean_compact_ptx_anchor:launch_bounds_min_blocks_2->3_after_true_wait_sync_restore`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_194601`
- round loop: `round 19/20`
- hypothesis: `The compact PTX anchor is now stable again, but it still sits at 201 regs/thread with occupancy limited to 2 CTAs/SM. Tightening only the PTX microkernel launch-bounds target from 2 to 3 may trim enough live state to improve latency hiding without changing grouped rows, stage depth, or the wait/sync cadence.`
- expected bottleneck: `Register-pressure-driven CTA residency remains the cleanest unresolved local bottleneck on the restored compact PTX surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2012`
- risk: `Moderate. The code edit is tiny, but forcing a tighter register budget can trade one latency problem for spills or a weaker instruction schedule.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_194414_bf16_gemm_v1_ac1299d7`
- latest runtime: `24.688641 ms`
- latest NCU analysis: `runs/20260421_194414_bf16_gemm_v1_ac1299d7/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.342` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.13` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.13` | barrier stalls are consuming 8.13% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__occupancy_limit_registers` `non_increasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Change only the compact PTX microkernel `__launch_bounds__(128, 2)` annotation to target 3 CTAs/SM.`
- `Leave grouped_rows=4, the clean wait/sync cadence, stage depth, and dispatch routing unchanged.`

## Delta vs previous run

- baseline run id: `20260421_194145_bf16_gemm_v1_f42c9310`
- stall `long_scoreboard` | delta `1.88` | trend `regressed`
- stall `barrier` | delta `0.27000000000000046` | trend `regressed`
- stall `mio_throttle` | delta `-0.13999999999999968` | trend `improved`
- stall `short_scoreboard` | delta `-0.1299999999999999` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.2799999999999976` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.10999999999999943` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `0.07000000000000028` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-0.05000000000000426` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
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
