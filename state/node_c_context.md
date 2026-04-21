# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the accepted PTX hot-band anchor after the failed live-state trim`
- candidate id: `diagnosis_20260421_114106:dir_01`
- base run id: `20260421_113859_bf16_gemm_v1_6668d21`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `restore_exact_f768e80_ptx_anchor_after_6668d21_loss`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_114106`
- round loop: `round 4/100`
- hypothesis: `The round-3 PTX live-state trim changed the wrong part of the recovered winner: despite a 2-register drop, active warps stayed flat and runtime exploded. Restoring the exact accepted PTX surface should recover the 24.293 ms anchor and re-establish a clean base for the next exploit.`
- expected bottleneck: `Known register-limited plateau on the accepted 128x128 PTX surface; this direction is a recovery step, not a new bottleneck attack.`
- code locations: `src/kernels/bf16_gemm_v1.cu, restore source commit: f768e80d950fa4cd036ea003b32af972278df540`
- risk: `low`
- metrics to re-check: `median runtime, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_113859_bf16_gemm_v1_6668d21`
- latest runtime: `46.366718 ms`
- latest NCU analysis: `runs/20260421_113859_bf16_gemm_v1_6668d21/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `198.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.63` | Occupancy is carrying metric Achieved Occupancy.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.37` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.336` | Tensor activity (48.36%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.36` | Tensor pipe activity is only 48.36% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.95` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.95` | barrier stalls are consuming 5.95% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.36` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.87` | long scoreboard stalls are consuming 6.87% of active warp issue slots.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.95` | barrier stalls are consuming 5.95% of active warp issue slots.

## Expected local changes

- `Restore the implementation surface from measured commit f768e80d950fa4cd036ea003b32af972278df540.`
- `Discard the round-3 scope-narrowing edit rather than layering another exploit on top of a loss surface.`
- `Keep the current workflow/workload support files on HEAD while only restoring compiled implementation code.`

## Delta vs previous run

- baseline run id: `20260421_111322_bf16_gemm_v1_f768e80`
- stall `barrier` | delta `0.4800000000000004` | trend `regressed`
- stall `long_scoreboard` | delta `-0.29000000000000004` | trend `improved`
- stall `mio_throttle` | delta `0.10000000000000009` | trend `regressed`
- stall `short_scoreboard` | delta `0.08999999999999986` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-2.16` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-2.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.0299999999999994` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-0.030000000000001137` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.

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
