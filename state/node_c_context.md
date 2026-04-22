# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Compact Two-Stage PTX Anchor After The Failed Wait-Sync-Collapse Variant`
- candidate id: `diagnosis_20260421_192742:dir_01`
- base run id: `20260421_192654_bf16_gemm_v1_40488b6e`
- primary family id: `restore_base::ptx_two_stage_anchor_after_failed_wait_sync_collapse`
- planned action fingerprint: `restore_compact_two_stage_ptx_anchor_after_wait_group_1_refill_before_wait_loss`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_192742`
- round loop: `round 14/20`
- hypothesis: `The latest wait-sync-collapse variant regressed from the restored compact anchor, so the next round should first return the code to the last known clean compact two-stage PTX seam before testing a different family.`
- expected bottleneck: `The immediate problem is the regressing wait_sync_collapse variant itself, which raised barrier and registers on the active compact surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2092-2120`
- risk: `Low. This is a narrow restore to the last clean compact PTX hot loop and does not change tiling, staging depth, or shared-memory budget.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`
- latest run id: `20260421_192654_bf16_gemm_v1_40488b6e`
- latest runtime: `24.845312 ms`
- latest NCU analysis: `runs/20260421_192654_bf16_gemm_v1_40488b6e/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `44.39` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.252` | Tensor activity (48.46%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.46` | Tensor pipe activity is only 48.46% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.84` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.84` | barrier stalls are consuming 8.84% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__occupancy_limit_registers` `non_decreasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Restore the compact PTX hot loop from the refill-before-wait variant back to the last clean two-stage anchor.`
- `Keep grouped_rows=4, the 128x128 dispatch, and the 22,016 B shared-memory footprint unchanged.`
- `Do not combine the restore with another sync-family tweak in the same round.`

## Delta vs previous run

- baseline run id: `20260421_192024_bf16_gemm_v1_8fd88cb4`
- stall `long_scoreboard` | delta `-4.9799999999999995` | trend `improved`
- stall `barrier` | delta `0.6400000000000006` | trend `regressed`
- stall `short_scoreboard` | delta `-0.4600000000000002` | trend `improved`
- stall `mio_throttle` | delta `0.40000000000000036` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `7.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.3999999999999986` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `0.060000000000002274` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.0600000000000005` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.

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
