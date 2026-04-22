# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Replace The Failed Interleaved PTX 64x64 Hot-Band Microkernel With The Compact Row-Pair Path`
- candidate id: `diagnosis_20260421_171314:dir_01`
- base run id: `20260421_170056_bf16_gemm_v1_13d24542`
- primary family id: `register_reuse::ptx_hotband_microkernel_live_range_reset`
- planned action fingerprint: `replace_interleaved_hotband_ptx_microkernel_with_compact_rowpair_accumulate_path`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_171314`
- round loop: `round 1/1`
- hypothesis: `The newly added outer-col-step interleave helper at `src/kernels/bf16_gemm_v1.cu:820-921` failed its own premise. Instead of shrinking the hot-band PTX live set, the measured run landed at 241 registers/thread and the hot-band kernel now dominates the NCU capture. Replacing that helper with the existing compact 64x64 PTX accumulate path (`ptx_wmma_accumulate_tile_set_64x64<false>`) or an equivalently scoped row-pair schedule should recover occupancy and most of the 6.55 ms regression without changing launch geometry, shared layout, or the row-group mapping.`
- expected bottleneck: `Register-pressure-driven occupancy collapse on the dominant hot-band PTX kernel: 241 registers/thread keeps the kernel at 2 CTAs/SM and leaves tensor utilization low despite unsaturated memory bandwidth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:733-922 (generic 64x64 PTX accumulate helper, failed interleaved helper, and dispatch wrapper), src/kernels/bf16_gemm_v1.cu:2080-2185 (bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel steady-state loop), src/kernels/bf16_gemm_v1.cu:2068-2185 (hot-band PTX store and loop callsite that now routes through the failed helper)`
- risk: `Moderate. The math path stays the same, but removing the interleaved helper can give back some of the intended B-fragment sharing or re-expose prior barrier pressure if the replacement is not kept compact.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, gpu__time_duration.sum`
- latest run id: `20260421_170056_bf16_gemm_v1_13d24542`
- latest runtime: `31.239679 ms`
- latest NCU analysis: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `48.4` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `43.24` | Tensor activity (37.48%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `37.48` | Tensor pipe activity is only 37.48% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.8` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.8` | barrier stalls are consuming 9.80% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `bounded_not_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Delete or bypass `ptx_wmma_accumulate_col_step_interleaved_64x64_ptx_microkernel` and stop routing the hot-band PTX kernel through that helper.`
- `Reuse the existing compact 64x64 PTX accumulate helper or a similarly scoped row-pair schedule so A/B fragment lifetimes stay local instead of being spread across the templated outer column loop.`
- `Leave grouped-row mapping, cp.async wide loads, and the current hot-band launch shape unchanged for the first validation pass.`

## Delta vs previous run

- baseline run id: `None`
- no structured stall delta is available
- no structured hotspot delta is available

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.

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
