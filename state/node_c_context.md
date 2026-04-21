# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Swap To The Single-K 128x128 Non-Microkernel Sibling`
- candidate id: `diagnosis_20260421_150910_round02_clean_7496aff2:dir_01`
- base run id: `20260421_150910_bf16_gemm_v1_7496aff2`
- primary family id: `kernel_variant::swap_to_nonmicrokernel_128x128`
- planned action fingerprint: `clean_ptx_hotband_baseline:microkernel->regular_128x128_single_k`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_150910_round02_clean_7496aff2`
- round loop: `round 2/10`
- hypothesis: `The grouped-row experiment showed that launch-order changes alone are not enough. The existing single-K 128x128 sibling keeps the accepted row split and one-K stage depth while changing the accumulate ordering away from the microkernel-specific path, which may reduce long-scoreboard waste directly.`
- expected bottleneck: `microkernel-specific accumulate ordering is contributing to long-scoreboard stalls on the accepted hot-band split`
- code locations: `src/kernels/bf16_gemm_v1.cu:1839, src/kernels/bf16_gemm_v1.cu:1924, src/kernels/bf16_gemm_v1.cu:1956, src/kernels/bf16_gemm_v1.cu:2114`
- risk: `Moderate risk: the variant is in-tree, but it still lacks a clean measurement on the accepted row split.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active`
- latest run id: `20260421_150910_bf16_gemm_v1_7496aff2`
- latest runtime: `24.537088 ms`
- latest NCU analysis: `runs/20260421_150910_bf16_gemm_v1_7496aff2/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.81` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.428` | Tensor activity (48.30%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.3` | Tensor pipe activity is only 48.30% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.33` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.33` | barrier stalls are consuming 5.33% of active warp issue slots.

## Guardrail metrics

- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `launch__occupancy_limit_registers` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Restore the grouped-row constant back to the clean accepted base if needed.`
- `Swap the default hot-band launch from the PTX microkernel path to the existing single-K non-microkernel 128x128 sibling.`

## Delta vs previous run

- baseline run id: `20260421_150626_bf16_gemm_v1_6cc462c4`
- stall `barrier` | delta `-0.1299999999999999` | trend `improved`
- stall `mio_throttle` | delta `0.1299999999999999` | trend `regressed`
- stall `long_scoreboard` | delta `0.08999999999999986` | trend `regressed`
- stall `short_scoreboard` | delta `0.009999999999999787` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-2.7300000000000004` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.5499999999999972` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.06999999999999318` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-0.03999999999999915` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.
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
