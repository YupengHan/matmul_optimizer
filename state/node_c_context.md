# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Transplant low-register half-panel staging into the correctness-safe 256x128 pivot`
- candidate id: `diagnosis_20260421_105526:dir_01`
- base run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- primary family id: `aggressive::transplant_half_panel_register_budget_into_the_correct_256x128_pivot`
- planned action fingerprint: `transplant_low_register_half_panel_ideas_into_safe_256x128_pivot_without_writer_split`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_105526`
- round loop: `round 1/100`
- hypothesis: `The richer NCU summary says the live queue should prioritize the only active family that directly attacks 200 registers per thread and the 16.63% active-warps ceiling. The correctness-safe 256x128 pivot should keep its current writer ownership, but transplant the compact staging and register-budget ideas that historically moved occupancy in the right direction.`
- expected bottleneck: `occupancy_latency_hiding_issue with tensor_core_underutilization driven by register pressure and oversized live state`
- code locations: `src/kernels/bf16_gemm_v1.cu:80 (FixedHotBandTile256x128 register/shared budget), src/kernels/bf16_gemm_v1.cu:1580 (bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel), src/kernels/bf16_gemm_v1.cu:1675 (256x128 export/store handoff)`
- risk: `High: this is the best hotspot-aligned family, but it touches a broader geometry and could reintroduce correctness or shared-budget regressions if the old ownership split leaks back in.`
- metrics to re-check: `sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, median runtime`
- latest run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- latest runtime: `24.186960 ms`
- latest NCU analysis: `runs/20260421_105134_bf16_gemm_v1_8dcab81/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `200.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.63` | Occupancy is carrying metric Achieved Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.13` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.77` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.296` | Tensor activity (48.40%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.4` | Tensor pipe activity is only 48.40% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.47` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.47` | barrier stalls are consuming 5.47% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.4` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `7.2` | Long scoreboard stalls are consuming 7.20% of active warp issue slots.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.47` | Barrier stalls are consuming 5.47% of active warp issue slots.

## Expected local changes

- `Compact the 256x128 live fragment footprint without reviving the broken half-panel writer split.`
- `Reduce accumulator or staging lifetime before touching export-side arithmetic.`
- `Keep the existing shared-memory budget discipline visible in the 256x128 path.`

## Delta vs previous run

- baseline run id: `20260421_105021_bf16_gemm_v1_8dcab81`
- stall `barrier` | delta `0.08000000000000007` | trend `regressed`
- stall `long_scoreboard` | delta `-0.03000000000000025` | trend `improved`
- stall `mio_throttle` | delta `0.010000000000000231` | trend `regressed`
- stall `short_scoreboard` | delta `0.0` | trend `flat`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.16000000000000014` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.020000000000003126` | trend `improved`
- hotspot delta: `new` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `N/A` | trend `new`
- hotspot delta: `disappeared` `Launch Statistics` | `Block Size` | delta `N/A` | trend `disappeared`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was improved in the improved bucket.

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
