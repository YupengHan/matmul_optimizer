# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Retime the PTX wait-group and CTA barrier seam on the current 128x128 anchor`
- candidate id: `diagnosis_20260421_114852:dir_01`
- base run id: `20260421_114455_bf16_gemm_v1_aaf076e`
- primary family id: `aggressive::trim_microkernel_barriers_without_x32_shared_blowup`
- planned action fingerprint: `retime_wait_group_and_sync_seam_on_current_128x128_ptx_anchor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_114852`
- round loop: `round 6/100`
- hypothesis: `The latest run is already sitting on the best measured current-workload PTX surface, but the active microkernel still spends 5.93% of active warp issue slots on barrier stalls while active warps remain stuck at 16.64%. The next bounded gain is to retime the `cp.async.wait_group` plus `__syncthreads()` seam inside the 128x128 PTX microkernel so the current two-stage pipeline hands off more cleanly without growing shared memory or reintroducing the higher-register control path.`
- expected bottleneck: `synchronization_barrier_issue layered on top of an occupancy_latency_hiding_issue in the active 128x128 PTX hot-band kernel`
- code locations: `src/kernels/bf16_gemm_v1.cu:1956-2064, src/kernels/bf16_gemm_v1.cu:2023-2056, src/kernels/bf16_gemm_v1.cu:338-359`
- risk: `medium`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`
- latest run id: `20260421_114455_bf16_gemm_v1_aaf076e`
- latest runtime: `46.532095 ms`
- latest NCU analysis: `runs/20260421_114455_bf16_gemm_v1_aaf076e/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `198.0` | The active hot-band PTX kernel is still register-limited at 198 registers per thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.64` | Achieved occupancy remains pinned near the theoretical floor, so barrier work must not hurt active warps.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.36` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.64` | Active warps are only 16.64% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.318` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.64%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.64` | Active warps are only 16.64% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.93` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.93` | barrier stalls are consuming 5.93% of active warp issue slots.

## Guardrail metrics

- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.64` | Barrier tuning is not worth taking if latency-hiding gets worse.
- `launch__occupancy_limit_registers` `non_increasing` from `2.0` | The local anchor already restored the lower-register surface; barrier retiming must not give that back.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.86` | A better handoff must not simply trade barrier time for worse scoreboard stalls.

## Expected local changes

- `Reschedule the `cp_async_wait_group_0()` and `__syncthreads()` placement inside the steady-state loop.`
- `Keep the two-stage shared-memory footprint unchanged.`
- `Preserve the current grouped-row mapping and PTX accumulator/export path while only tightening the handoff seam.`

## Delta vs previous run

- baseline run id: `20260421_114147_bf16_gemm_v1_4784c8d`
- stall `barrier` | delta `0.35999999999999943` | trend `regressed`
- stall `long_scoreboard` | delta `-0.08999999999999986` | trend `improved`
- stall `short_scoreboard` | delta `0.050000000000000266` | trend `regressed`
- stall `mio_throttle` | delta `0.03000000000000025` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-2.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.0599999999999987` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.07000000000000028` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-0.030000000000001137` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
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
