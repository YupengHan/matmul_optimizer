# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot`
- candidate id: `diagnosis_20260421_153357_round05_clean_f1c576ee:dir_01`
- base run id: `20260421_153357_bf16_gemm_v1_f1c576ee`
- primary family id: `aggressive::transplant_half_panel_register_budget_into_the_correct_256x128_pivot`
- planned action fingerprint: `restore_correct_256x128_pivot_surface_then_transplant_low_reg_half_panel_staging_without_writer_split`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_153357_round05_clean_f1c576ee`
- round loop: `round 5/10`
- hypothesis: `The failed 256x128 pivot promotion proved that geometry alone is not enough, but it also proved that 256x128 can slash registers and long-scoreboard cost. The coherent follow-on is to keep the correctness-safe 256x128 pivot ownership path and transplant only the low-register staging and reuse ideas that the archived half-panel branch got right, without reviving the writer split that broke correctness.`
- expected bottleneck: `Register footprint, stage design, and reuse efficiency inside the 256x128 hot-band path are still the missing pieces preventing the human-guided tiling family from becoming viable.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1580-1676, src/kernels/bf16_gemm_v1.cu:539-693, src/kernels/bf16_gemm_v1.cu:903-995`
- risk: `High. This is the highest-ceiling family left in the repo, but it touches the same 256x128 control/export surface that has failed correctness before.`
- metrics to re-check: `correctness on all 3 dataset cases before trusting runtime, launch__registers_per_thread, launch__shared_mem_per_block_allocated, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, median runtime`
- latest run id: `20260421_153357_bf16_gemm_v1_f1c576ee`
- latest runtime: `30.173615 ms`
- latest NCU analysis: `runs/20260421_153357_bf16_gemm_v1_f1c576ee/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `43.902` | Tensor activity (36.77%) is low relative to available memory bandwidth, and active warps (16.66%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `36.77` | Tensor pipe activity is only 36.77% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- `occupancy_latency_hiding_issue` | severity `36.14` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `1.0` | Register pressure is limiting occupancy to 1 blocks per SM.
- `synchronization_barrier_issue` | severity `8.32` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Restore the correctness-safe 256x128 pivot ownership path.`
- `Transplant only the low-register staging and reuse behavior from the archived half-panel branch without reviving split-writer ownership.`

## Delta vs previous run

- baseline run id: `20260421_153021_bf16_gemm_v1_24f31aab`
- stall `long_scoreboard` | delta `-5.02` | trend `improved`
- stall `short_scoreboard` | delta `4.529999999999999` | trend `regressed`
- stall `barrier` | delta `2.83` | trend `regressed`
- stall `mio_throttle` | delta `-2.73` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-29.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-13.190000000000005` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-13.159999999999997` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-11.939999999999998` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
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
