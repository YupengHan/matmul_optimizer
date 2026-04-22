# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 128x128x32 Two-K-Stage Hot-Band Kernel From The Clean Compact Anchor`
- candidate id: `diagnosis_20260421_193427:dir_01`
- base run id: `20260421_193214_bf16_gemm_v1_5bbcf7bf`
- primary family id: `async_copy::ptx_hotband_two_k_stage_pg2s`
- planned action fingerprint: `launch_fixed_hot_band:compact_ptx_anchor->existing_128x128x32_guarded_probe_from_24p682`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_193427`
- round loop: `round 16/20`
- hypothesis: `The branch is no longer obviously missing one tiny compact barrier trim. A bounded way to test a broader latency-hiding change is to switch the fixed hot-band dispatch to the existing 128x128x32 two-K-stage kernel and see whether amortizing the copy/sync cadence across two K tiles helps more than the current single-K compact PTX path.`
- expected bottleneck: `The unresolved bottleneck is still latency hiding and copy/sync amortization on the accepted compact surface, not a new geometry family.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1722-1883, src/kernels/bf16_gemm_v1.cu:2154-2203`
- risk: `Moderate-high. This stays on the 128x128 hot-band geometry, but it increases the staging footprint and changes the hot-band pipeline shape materially.`
- metrics to re-check: `median runtime, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_193214_bf16_gemm_v1_5bbcf7bf`
- latest runtime: `24.882688 ms`
- latest NCU analysis: `runs/20260421_193214_bf16_gemm_v1_5bbcf7bf/ncu_analysis.json`

## Relevant hotspots

- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.04` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.56` | Active warps are only 16.56% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.492` | Tensor activity (48.26%) is low relative to available memory bandwidth, and active warps (16.56%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.26` | Tensor pipe activity is only 48.26% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.56` | Active warps are only 16.56% of peak sustained active.
- `synchronization_barrier_issue` | severity `7.86` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `7.86` | barrier stalls are consuming 7.86% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A
- `launch__occupancy_limit_registers` `bounded_not_materially_worse_than_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `bounded_not_materially_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Switch the fixed hot-band dispatch from the compact PTX microkernel to the existing 128x128x32 staged kernel.`
- `Keep grouped_rows=4, the peeled row band, and the 64x96 tail unchanged.`
- `Do not combine the staged-kernel launch with another compact sync-family rewrite in the same round.`

## Delta vs previous run

- baseline run id: `20260421_192933_bf16_gemm_v1_09758191`
- stall `long_scoreboard` | delta `-1.8600000000000003` | trend `improved`
- stall `barrier` | delta `-0.28000000000000025` | trend `improved`
- stall `short_scoreboard` | delta `0.1299999999999999` | trend `regressed`
- stall `mio_throttle` | delta `0.1200000000000001` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.5399999999999991` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.11999999999999744` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-0.07000000000000028` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.03999999999999915` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was regressed in the regressed bucket.

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
