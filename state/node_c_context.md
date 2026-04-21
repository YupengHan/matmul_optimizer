# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Re-anchor on the best measured PTX surface under the current workload`
- candidate id: `diagnosis_20260421_114422:dir_01`
- base run id: `20260421_114147_bf16_gemm_v1_4784c8d`
- primary family id: `legacy::reanchor_the_current_workload_ptx_surface`
- planned action fingerprint: `restore_exact_6668d21_as_current_workload_anchor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_114422`
- round loop: `round 5/100`
- hypothesis: `The current workload has drifted enough that the old historical accepted base is no longer a valid recovery target. Restoring the slightly faster 20260421_113859_bf16_gemm_v1_6668d21 PTX variant should establish a sane current-workload anchor before more exploits are layered on top.`
- expected bottleneck: `Current-workload re-anchoring step; establishes the local PTX baseline before the next bounded barrier exploit.`
- code locations: `src/kernels/bf16_gemm_v1.cu, restore source commit: 6668d2193f6619c3de1cc6000711a62fc1f0fcd8`
- risk: `low`
- metrics to re-check: `median runtime, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_114147_bf16_gemm_v1_4784c8d`
- latest runtime: `46.509056 ms`
- latest NCU analysis: `runs/20260421_114147_bf16_gemm_v1_4784c8d/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `200.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Occupancy is carrying metric Achieved Occupancy.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.77` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.306` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.57` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.57` | barrier stalls are consuming 5.57% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.39` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.95` | long scoreboard stalls are consuming 6.95% of active warp issue slots.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.57` | barrier stalls are consuming 5.57% of active warp issue slots.

## Expected local changes

- `Restore the implementation surface from measured commit 6668d2193f6619c3de1cc6000711a62fc1f0fcd8.`
- `Treat this as current-workload anchoring, not as a regression recovery toward the stale 24 ms history.`
- `Preserve workflow/workload support files on HEAD while only restoring compiled implementation code.`

## Delta vs previous run

- baseline run id: `20260421_113859_bf16_gemm_v1_6668d21`
- stall `barrier` | delta `-0.3799999999999999` | trend `improved`
- stall `long_scoreboard` | delta `0.08000000000000007` | trend `regressed`
- stall `short_scoreboard` | delta `-0.06000000000000005` | trend `improved`
- stall `mio_throttle` | delta `-0.050000000000000266` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `2.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `1.5500000000000007` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.9900000000000002` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.030000000000001137` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
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
