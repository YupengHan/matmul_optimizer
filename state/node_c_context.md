# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Swap The Recovered PTX Hot-Band Back To The Regular 128x128 Single-K Sibling`
- candidate id: `diagnosis_20260421_175153:dir_01`
- base run id: `20260421_172601_bf16_gemm_v1_117cd3e7`
- primary family id: `kernel_variant::swap_to_nonmicrokernel_128x128`
- planned action fingerprint: `compact_ptx_hotband_recovery:microkernel->regular_128x128_single_k_sibling`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_175153`
- round loop: `round 1/20`
- hypothesis: `The compact PTX row-pair reset removed the worst regression, but the current hot-band microkernel still sits at 202 registers/thread and only 16.59% active warps. The existing single-K 128x128 sibling keeps the same CTA geometry and one-K staging depth while using the regular 64x64 accumulate helper instead of the microkernel-specific consume order. Repo history already measured this sibling at a slightly lower register footprint (196 regs/thread) and a small win on the clean baseline, so it is the best next local exploit on the current branch.`
- expected bottleneck: `Microkernel-specific consume ordering and residual accumulator live range on the dominant 128x128 hot-band path are still holding occupancy to the 2-CTA class.`
- code locations: `src/kernels/bf16_gemm_v1.cu:734-829, src/kernels/bf16_gemm_v1.cu:1876-1988, src/kernels/bf16_gemm_v1.cu:1990-2094, src/kernels/bf16_gemm_v1.cu:2144-2151`
- risk: `Moderate. The sibling is already in-tree and has prior positive evidence, but the branch currently carries the compact PTX recovery rather than the old clean baseline, so the win size may be smaller than before.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_172601_bf16_gemm_v1_117cd3e7`
- latest runtime: `24.806945 ms`
- latest NCU analysis: `runs/20260421_172601_bf16_gemm_v1_117cd3e7/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.21` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.368` | Tensor activity (48.36%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.36` | Tensor pipe activity is only 48.36% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.39` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.39` | barrier stalls are consuming 6.39% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing` from `N/A` | N/A
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Keep the current 128x128 hot-band launch region and one-K staging depth.`
- `Route the dominant hot-band launch back to the regular 128x128 single-K sibling instead of the compact PTX microkernel wrapper.`
- `Leave grouped rows, cp.async widths, and the 64x384 / 64x96 side paths unchanged for the first validation pass.`

## Delta vs previous run

- baseline run id: `20260421_170056_bf16_gemm_v1_13d24542`
- stall `mio_throttle` | delta `-11.41` | trend `improved`
- stall `barrier` | delta `-3.410000000000001` | trend `improved`
- stall `short_scoreboard` | delta `-1.3299999999999998` | trend `improved`
- stall `long_scoreboard` | delta `0.8900000000000006` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-39.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-12.669999999999995` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `10.96` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `5.539999999999999` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` | Previous delta was regressed in the regressed bucket.

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
