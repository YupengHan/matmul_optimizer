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
- round loop: `round 10/10`
- latest run id: `20260421_160237_bf16_gemm_v1_404e8c44`
- latest runtime: `25.996288 ms`
- latest NCU analysis: `runs/20260421_160237_bf16_gemm_v1_404e8c44/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.06` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.77` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.95` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.43` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.744` | Tensor activity (46.44%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.44` | Tensor pipe activity is only 46.44% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.16` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.16` | barrier stalls are consuming 10.16% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.23` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `46.44` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `24.77` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `10.16` | barrier stalls are consuming 10.16% of active warp issue slots.
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `6.74` | short scoreboard stalls are consuming 6.74% of active warp issue slots.

## Expected local changes

- no direction-specific local change notes were provided

## Delta vs previous run

- baseline run id: `20260421_160001_bf16_gemm_v1_d7576a6e`
- stall `short_scoreboard` | delta `2.0300000000000002` | trend `regressed`
- stall `barrier` | delta `-1.0700000000000003` | trend `improved`
- stall `long_scoreboard` | delta `0.33000000000000007` | trend `regressed`
- stall `mio_throttle` | delta `-0.20999999999999996` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-7.3100000000000005` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-0.3500000000000014` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.240000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.11999999999999744` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was regressed in the regressed bucket.

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
