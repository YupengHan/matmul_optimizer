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
- round loop: `round 13/20`
- latest run id: `20260421_192024_bf16_gemm_v1_8fd88cb4`
- latest runtime: `24.693696 ms`
- latest NCU analysis: `runs/20260421_192024_bf16_gemm_v1_8fd88cb4/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `201.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.5` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.63` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.02` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.26` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.322` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.2` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.2` | barrier stalls are consuming 8.20% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.39` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.61` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `8.2` | barrier stalls are consuming 8.20% of active warp issue slots.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `5.17` | long scoreboard stalls are consuming 5.17% of active warp issue slots.

## Expected local changes

- no direction-specific local change notes were provided

## Delta vs previous run

- baseline run id: `20260421_191613_bf16_gemm_v1_9652b835`
- stall `short_scoreboard` | delta `-4.359999999999999` | trend `improved`
- stall `mio_throttle` | delta `3.16` | trend `regressed`
- stall `long_scoreboard` | delta `2.98` | trend `regressed`
- stall `barrier` | delta `-0.120000000000001` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `34.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `13.400000000000006` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `13.299999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `11.82` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
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

- no active direction selected yet; use `python scripts/graph.py select-next` or `python scripts/graph.py use-recommended-direction` before using the dirty-path guardrail
