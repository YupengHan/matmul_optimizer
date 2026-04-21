# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 256x128 Pivot Hot-Band Kernel`
- candidate id: `diagnosis_20260421_153021_round04_clean_24f31aab:dir_01`
- base run id: `20260421_153021_bf16_gemm_v1_24f31aab`
- primary family id: `legacy::promote_the_existing_256x128_pivot_hot_band_kernel`
- planned action fingerprint: `538fb586502fa3b4`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_153021_round04_clean_24f31aab`
- round loop: `round 4/10`
- hypothesis: `The 128x128 family has now delivered two incremental wins without moving achieved warps or occupancy limits. The cleanest next structural test is to route the default hot-band launch onto the existing 256x128 pivot kernel so the search directly tests the human-guided 256x128 / 64x64 tiling preference and a materially different CTA geometry on the accepted clean base.`
- expected bottleneck: `Current four-warp 128x128 CTA geometry is capping residency and CTA-count efficiency on the hot-band region more than local pointer arithmetic is.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1580-1683, src/kernels/bf16_gemm_v1.cu:2090-2138`
- risk: `Moderate. The kernel already exists and aligns with the human tiling guidance, but a larger CTA can still lose if it bloats the live set or export path.`
- metrics to re-check: `median runtime, kernel name and grid size in ncu_metrics.csv, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_153021_bf16_gemm_v1_24f31aab`
- latest runtime: `24.195072 ms`
- latest NCU analysis: `runs/20260421_153021_bf16_gemm_v1_24f31aab/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `41.99` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.382` | Tensor activity (48.33%) is low relative to available memory bandwidth, and active warps (16.61%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.33` | Tensor pipe activity is only 48.33% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.61` | Active warps are only 16.61% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.49` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.49` | barrier stalls are consuming 5.49% of active warp issue slots.

## Guardrail metrics

- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `launch__registers_per_thread` `watch` from `N/A` | N/A

## Expected local changes

- `Swap the default hot-band launch from the current 128x128 regular sibling to the existing 256x128 pivot kernel.`
- `Keep the residual row-band and tail handling unchanged for the first measurement.`

## Delta vs previous run

- baseline run id: `20260421_152228_bf16_gemm_v1_2fbb368d`
- stall `long_scoreboard` | delta `0.05999999999999961` | trend `regressed`
- stall `mio_throttle` | delta `-0.020000000000000018` | trend `improved`
- stall `barrier` | delta `0.009999999999999787` | trend `regressed`
- stall `short_scoreboard` | delta `0.0` | trend `flat`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.34999999999999787` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.03999999999999915` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-0.019999999999999574` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.019999999999999574` | trend `improved`

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

- `src/kernels/bf16_gemm_v1.cu`
