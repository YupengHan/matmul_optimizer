# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Reopen The Writer-Safe 256x128 64x64-Warp Hot-Band Branch From The Current Compact PTX Base`
- candidate id: `diagnosis_20260421_191121:dir_01`
- base run id: `20260421_190652_bf16_gemm_v1_88a8acfc`
- primary family id: `tiling::hotband_256x128_reopen`
- planned action fingerprint: `reopen_256x128_64x64_warp_hotband_from_24p689_compact_ptx_plateau`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_191121`
- round loop: `round 11/20`
- hypothesis: `The current 128x128 PTX surface is no longer obviously broken, but it is still capped by a 201-register, 2-CTA occupancy ceiling and only 16.61% active warps. Reopening the correctness-safe 256x128 / 64x64-warp branch from the current compact PTX base is the cleanest way to test whether the remaining gap is geometric and reuse-related rather than another tiny wait/sync tweak.`
- expected bottleneck: `The dominant ceiling is occupancy and hot-band geometry on the active 128x128 PTX path, not raw DRAM bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1616-1714, src/kernels/bf16_gemm_v1.cu:2154-2203`
- risk: `Moderate-high. This is a structural reopen that changes hot-band CTA geometry and export scheduling, but it stays on the writer-safe path already present in source.`
- metrics to re-check: `correctness on all dataset cases, median runtime, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_190652_bf16_gemm_v1_88a8acfc`
- latest runtime: `24.689153 ms`
- latest NCU analysis: `runs/20260421_190652_bf16_gemm_v1_88a8acfc/ncu_analysis.json`

## Relevant hotspots

- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A
- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.322` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.14` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.14` | barrier stalls are consuming 8.14% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `bounded_not_materially_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Switch the fixed hot-band dispatch from the compact 128x128 PTX microkernel to the existing writer-safe 256x128 kernel.`
- `Keep the peeled 64x384 row band and 64x96 tail unchanged on the first measurement.`
- `Preserve async-copy staging and the right-left-right-left warp ownership path already embedded in the 256x128 kernel.`

## Delta vs previous run

- baseline run id: `20260421_190032_bf16_gemm_v1_9e21c98f`
- stall `long_scoreboard` | delta `4.97` | trend `regressed`
- stall `barrier` | delta `-0.8200000000000003` | trend `improved`
- stall `short_scoreboard` | delta `0.5` | trend `regressed`
- stall `mio_throttle` | delta `-0.3899999999999997` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-7.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.19000000000000128` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-0.07000000000000028` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.060000000000002274` | trend `regressed`

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
