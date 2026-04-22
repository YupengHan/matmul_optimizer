# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Skip The Final No-Refill CTA Sync On The Compact PTX Anchor`
- candidate id: `diagnosis_20260421_193031:dir_01`
- base run id: `20260421_192933_bf16_gemm_v1_09758191`
- primary family id: `sync_pipeline::trim_microkernel_barriers_without_shared_blowup`
- planned action fingerprint: `compact_two_stage_ptx_hotband:skip_final_no_refill_sync_after_penultimate_tile`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_193031`
- round loop: `round 15/20`
- hypothesis: `On the penultimate tile, the current compact PTX loop still pays cp_async_wait_group_0 plus __syncthreads even though future_tile_idx is already out of range and no shared stage will be overwritten. Skipping that final no-refill sync should remove one CTA barrier from the steady-state path without changing registers, stage depth, or the shared-memory budget.`
- expected bottleneck: `The remaining local tax is unnecessary final-drain barrier overhead on the accepted compact PTX surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2106-2119`
- risk: `Low-to-moderate. This is a tiny control-path trim, but it still changes CTA synchronization semantics on the last steady-state handoff.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`
- latest run id: `20260421_192933_bf16_gemm_v1_09758191`
- latest runtime: `24.682431 ms`
- latest NCU analysis: `runs/20260421_192933_bf16_gemm_v1_09758191/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.342` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.14` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.14` | barrier stalls are consuming 8.14% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__occupancy_limit_registers` `non_decreasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Special-case the penultimate-tile handoff so the loop skips the final no-refill __syncthreads.`
- `Keep the compact 128x128 PTX dispatch, grouped_rows=4, and 22,016 B shared-memory footprint unchanged.`
- `Do not combine this trim with any wait_group_1 or refill-before-wait rewrite.`

## Delta vs previous run

- baseline run id: `20260421_192654_bf16_gemm_v1_40488b6e`
- stall `long_scoreboard` | delta `5.01` | trend `regressed`
- stall `barrier` | delta `-0.6999999999999993` | trend `improved`
- stall `short_scoreboard` | delta `0.47` | trend `regressed`
- stall `mio_throttle` | delta `-0.39000000000000057` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-7.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.33999999999999986` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-0.08999999999999986` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-0.05000000000000426` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was improved in the improved bucket.

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
