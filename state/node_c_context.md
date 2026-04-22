# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore A Compact Two-Stage PTX Ring While Keeping Grouped Rows At 2`
- candidate id: `diagnosis_20260421_184831:dir_01`
- base run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- primary family id: `sync_pipeline::ptx_two_stage_restore_keep_grouped_rows_2`
- planned action fingerprint: `restore_compact_ptx_two_stage_ring_keep_grouped_rows_2_after_failed_drain_split`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_184831`
- round loop: `round 7/20`
- hypothesis: `The latest regression is dominated by register-pressure and occupancy collapse from the duplicated 3-stage split loop, not by grouped_rows=2 itself. Dropping back to a compact two-stage PTX ring while keeping grouped_rows=2 should recover a large chunk of the 57-register spike and tell us whether the row-group retune can help once the hot path is lean again.`
- expected bottleneck: `Registers-per-thread and occupancy are the first bottlenecks to remove; barrier cleanup is no longer the primary limiter after the round-6 regression.`
- code locations: `src/kernels/bf16_gemm_v1.cu:156, src/kernels/bf16_gemm_v1.cu:2005-2138`
- risk: `Low to moderate. This stays on the active PTX dispatch path, but it rewrites stage-count and drain control together and still has correctness risk if the two-stage wait cadence is restored incorrectly.`
- metrics to re-check: `median runtime, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`
- latest run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- latest runtime: `28.767664 ms`
- latest NCU analysis: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `48.43` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `33.884` | Tensor activity (46.86%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.86` | Tensor pipe activity is only 46.86% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.72` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.72` | barrier stalls are consuming 6.72% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing_vs_current_run` from `N/A` | N/A
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Reduce the PTX hot-band ring from 3 stages back to 2.`
- `Remove the split steady-state and drain loop duplication that inflated the live register set.`
- `Keep kFixedHotBandPtxGroupedRows at 2 during the first two-stage reset.`

## Delta vs previous run

- baseline run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- stall `mio_throttle` | delta `1.2599999999999998` | trend `regressed`
- stall `barrier` | delta `-0.8700000000000001` | trend `improved`
- stall `short_scoreboard` | delta `-0.42999999999999994` | trend `improved`
- stall `long_scoreboard` | delta `-0.09` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `57.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `21.460000000000004` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `2.240000000000002` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-1.2299999999999969` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
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
