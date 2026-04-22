# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `None`
- direction name: `N/A`
- candidate id: `None`
- base run id: `None`
- primary family id: `None`
- planned action fingerprint: `None`
- selection mode: `None`
- source diagnosis id: `None`
- round loop: `round 17/20`
- latest run id: `20260421_193649_bf16_gemm_v1_fd009266`
- latest runtime: `31.612928 ms`
- latest NCU analysis: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `213.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `26.65` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `35.12` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `39.98` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `45.43` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `40.534` | Tensor activity (40.21%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `40.21` | Tensor pipe activity is only 40.21% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.85` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.85` | barrier stalls are consuming 9.85% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `40.21` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.57` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `9.85` | barrier stalls are consuming 9.85% of active warp issue slots.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `7.32` | long scoreboard stalls are consuming 7.32% of active warp issue slots.

## Expected local changes

- no direction-specific local change notes were provided

## Delta vs previous run

- baseline run id: `20260421_193214_bf16_gemm_v1_5bbcf7bf`
- stall `long_scoreboard` | delta `3.9800000000000004` | trend `regressed`
- stall `mio_throttle` | delta `2.2` | trend `regressed`
- stall `barrier` | delta `1.9899999999999993` | trend `regressed`
- stall `short_scoreboard` | delta `-0.1599999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `22.61` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `12.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-7.8700000000000045` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-6.460000000000001` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.

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

- no active direction selected yet; use `python scripts/graph.py select-next` or `python scripts/graph.py use-recommended-direction` before using the dirty-path guardrail
