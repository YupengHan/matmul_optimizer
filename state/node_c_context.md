# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Force 3-CTA Residency On The Non-PTX 128x128 Sibling`
- candidate id: `diagnosis_20260421_155253:dir_01`
- base run id: `20260421_155210_bf16_gemm_v1_9cac32cb`
- primary family id: `aggressive::force_three_cta_residency_on_the_non_ptx_128x128_sibling`
- planned action fingerprint: `restore_non_ptx_128x128_sibling_surface_then_raise_launch_bounds_to_three_cta_residency`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_155253`
- round loop: `round 7/10`
- hypothesis: `Round 6 proved that recovering from the losing 256x128 branch was the right call, but it also showed that the PTX-local export batching variant is still not the best 128x128 surface. The accepted base remains the non-PTX 128x128 sibling at 24.195072 ms. The cleanest next probe is therefore to restore that sibling and test whether a 3-CTA launch-bounds target can improve latency hiding there without paying the PTX microkernel export tax that kept round 6 slightly above the accepted base.`
- expected bottleneck: `Register-limited occupancy and latency hiding on the accepted non-PTX 128x128 hot-band surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1869-1981, src/kernels/bf16_gemm_v1.cu:2139-2147`
- risk: `Moderate. The restore surface is correctness-safe and already faster than the current run, but the 3-CTA budget can still trade registers for spills or barrier regressions.`
- metrics to re-check: `correctness on all 3 dataset cases before trusting runtime, median runtime versus the 24.195072 ms accepted base, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, gpu__time_duration.sum`
- latest run id: `20260421_155210_bf16_gemm_v1_9cac32cb`
- latest runtime: `24.346112 ms`
- latest NCU analysis: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.77` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.316` | Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.38` | Tensor pipe activity is only 48.38% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.61` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.61` | barrier stalls are consuming 5.61% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A

## Expected local changes

- `Restore the accepted non-PTX 128x128 sibling launch path.`
- `Raise the non-PTX sibling launch-bounds target to probe whether 3-CTA residency is viable on the accepted base.`

## Delta vs previous run

- baseline run id: `20260421_154110_bf16_gemm_v1_afe26c16`
- stall `long_scoreboard` | delta `4.9` | trend `regressed`
- stall `short_scoreboard` | delta `-4.68` | trend `improved`
- stall `mio_throttle` | delta `2.94` | trend `regressed`
- stall `barrier` | delta `-2.71` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `33.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `13.220000000000006` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `13.149999999999999` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `11.7` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
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
