# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim live state inside the recovered 128x128 PTX hot-band control path`
- candidate id: `diagnosis_20260421_113657:dir_01`
- base run id: `20260421_111322_bf16_gemm_v1_f768e80`
- primary family id: `legacy::retune_the_active_ptx_one_k_128x128_hot_band_control_path`
- planned action fingerprint: `trim_live_state_and_stage_pointer_lifetime_in_128x128_ptx_microkernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_113657`
- round loop: `round 3/100`
- hypothesis: `If the recovered PTX winner drops a small amount of register lifetime in the steady-state loop, achieved warps should rise above the current 16.63% plateau without reopening the round-1 256x128 regression.`
- expected bottleneck: `occupancy_latency_hiding_issue with a secondary tensor_core_underutilization component on the accepted 128x128 PTX hot-band path`
- code locations: `src/kernels/bf16_gemm_v1.cu:1956, src/kernels/bf16_gemm_v1.cu:1983, src/kernels/bf16_gemm_v1.cu:2021`
- risk: `medium`
- metrics to re-check: `launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, median runtime`
- latest run id: `20260421_111322_bf16_gemm_v1_f768e80`
- latest runtime: `24.293376 ms`
- latest NCU analysis: `runs/20260421_111322_bf16_gemm_v1_f768e80/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `200.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.63` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.77` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.286` | Tensor activity (48.41%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.41` | Tensor pipe activity is only 48.41% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.47` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.47` | barrier stalls are consuming 5.47% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.41` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `7.16` | long scoreboard stalls are consuming 7.16% of active warp issue slots.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.47` | barrier stalls are consuming 5.47% of active warp issue slots.

## Expected local changes

- `Shorten the lifetime of grouped-row / pid / future-tile temporaries around the PTX steady-state loop.`
- `Avoid keeping both next-tile and future-tile address chains live across the accumulate call when one can be recomputed in a narrower scope.`
- `Keep the recovered grouped-row mapping intact while trimming control-path live state.`

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
