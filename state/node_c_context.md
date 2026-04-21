# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Accepted Base And Expand The 64x384 Row Band`
- candidate id: `diagnosis_20260421_142317_round02_5ea07e35:dir_01`
- base run id: `20260421_142317_bf16_gemm_v1_5ea07e35`
- primary family id: `tiling_decomposition::expand_64x384_row_band`
- planned action fingerprint: `restore_ptx_hotband_baseline:6400_pivot_rows->smaller_pivot_more_64x384_rows`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_142317_round02_5ea07e35`
- round loop: `round 2/10`
- hypothesis: `The accepted PTX hot-band launch is still the best measured baseline, but too much of the fixed shape remains on the 128x128 hotspot. Restoring that baseline and reducing kFixedPivotHotRows should move more work into the historically stronger 64x384 peeled path, cutting aggregate barrier exposure without reintroducing the staged-128x128 regression.`
- expected bottleneck: `too much of the fixed hot band is assigned to the 128x128 PTX hotspot instead of the stronger 64x384 family`
- code locations: `src/kernels/bf16_gemm_v1.cu:152, src/kernels/bf16_gemm_v1.cu:153, src/kernels/bf16_gemm_v1.cu:1956, src/kernels/bf16_gemm_v1.cu:2110, src/kernels/bf16_gemm_v1.cu:2122`
- risk: `Moderate risk: the historical 64x384 sweep predates the newest PTX hot-band refinements, so moving too many rows may simply shift the bottleneck instead of shrinking it.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__throughput.avg.pct_of_peak_sustained_elapsed, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`
- latest run id: `20260421_142317_bf16_gemm_v1_5ea07e35`
- latest runtime: `30.007680 ms`
- latest NCU analysis: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `45.22` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `40.616` | Tensor activity (40.12%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `40.12` | Tensor pipe activity is only 40.12% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.09` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.09` | barrier stalls are consuming 10.09% of active warp issue slots.

## Guardrail metrics

- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `sm__throughput.avg.pct_of_peak_sustained_elapsed` `non_decreasing` from `N/A` | N/A

## Expected local changes

- `Restore the default fixed-shape hot-band launch from the regressed 128x128x32 staged sibling back to the accepted PTX hot-band kernel.`
- `Lower kFixedPivotHotRows so more hot-band rows run through the 64x384 peeled path while keeping the 64x96 tail unchanged.`

## Delta vs previous run

- baseline run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- stall `barrier` | delta `4.6` | trend `regressed`
- stall `long_scoreboard` | delta `-1.62` | trend `improved`
- stall `mio_throttle` | delta `1.1999999999999997` | trend `regressed`
- stall `short_scoreboard` | delta `0.54` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `12.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-8.160000000000004` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-5.630000000000003` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-5.57` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
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

- `CMakeLists.txt`
- `src/kernels/bf16_gemm_v1.cu`
