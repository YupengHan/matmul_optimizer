# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `seed_01`
- direction name: `Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup`
- candidate id: `seed_master_history_round02_01:seed_01`
- base run id: `20260421_150626_bf16_gemm_v1_6cc462c4`
- primary family id: `aggressive::trim_microkernel_barriers_without_x32_shared_blowup`
- planned action fingerprint: `restore_three_cta_microkernel_surface_then_trim_wait_sync_cadence_without_two_k_stage_buffers`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_013500`
- round loop: `round 2/20`
- hypothesis: `Round 29 and round 30 together now fence off both obvious extremes on the 128x128 occupancy-first path. The launch-bounds probe reduced registers successfully but doubled barrier cost. The two-K-stage kernel reduced per-stage synchronization pressure but doubled shared-memory footprint enough to destroy the occupancy gain. That leaves one bounded but still aggressive follow-up family: keep the smaller 22,016 B shared-memory microkernel footprint from round 29 and attack the barrier cost more surgically through wait/sync cadence or export scheduling rather than by introducing a second full K-tile buffer pair.`
- expected bottleneck: `Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the lower shared-memory footprint.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1955-2060`
- risk: `High. This is a more manual PTX-microkernel surgery path than the exact restore.`
- metrics to re-check: `hot-band launch__shared_mem_per_block_allocated, hot-band launch__registers_per_thread, hot-band smsp__warp_issue_stalled_barrier_per_warp_active.pct, hot-band sm__warps_active.avg.pct_of_peak_sustained_active, hot-band gpu__time_duration.sum`
- latest run id: `20260421_175700_bf16_gemm_v1_05086a14`
- latest runtime: `26.385408 ms`
- latest NCU analysis: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.06` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.77` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.95` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.42` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.724` | Tensor activity (46.46%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.46` | Tensor pipe activity is only 46.46% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.15` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.15` | barrier stalls are consuming 10.15% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.23` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `46.46` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `24.77` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `10.15` | barrier stalls are consuming 10.15% of active warp issue slots.
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `6.74` | short scoreboard stalls are consuming 6.74% of active warp issue slots.

## Expected local changes

- no direction-specific local change notes were provided

## Delta vs previous run

- baseline run id: `20260421_172601_bf16_gemm_v1_117cd3e7`
- stall `short_scoreboard` | delta `4.88` | trend `regressed`
- stall `barrier` | delta `3.7600000000000007` | trend `regressed`
- stall `long_scoreboard` | delta `-3.2700000000000005` | trend `improved`
- stall `mio_throttle` | delta `-2.21` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-34.0` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Theoretical Occupancy` | delta `8.329999999999998` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `8.190000000000001` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.5500000000000007` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was improved in the improved bucket.

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
