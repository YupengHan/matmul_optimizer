# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Promote The Existing 128x128x32 Staged Hot-Band Kernel`
- candidate id: `diagnosis_20260421_133418_round01_c859cd06:dir_01`
- base run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- primary family id: `sync_pipeline::hotband_128x128_stage_swap`
- planned action fingerprint: `launch_fixed_hot_band:ptx128x128_microkernel->staged_128x128x32`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_133418_round01_c859cd06`
- round loop: `round 1/10`
- hypothesis: `The current default hot-band kernel is paying too much synchronization and wait overhead per 16-wide K tile. The existing 128x128x32 staged sibling already consumes two K tiles per stage and should reduce barrier and long-scoreboard pressure in the dominant hot-band region without changing the overall 128x128 CTA footprint.`
- expected bottleneck: `synchronization_barrier_issue and long_scoreboard latency in the current hot-band 128x128 PTX microkernel`
- code locations: `src/kernels/bf16_gemm_v1.cu:1685, src/kernels/bf16_gemm_v1.cu:2102`
- risk: `Low-to-moderate risk: the kernel already exists, but the alternate staging schedule may trade barrier relief for higher shared-memory traffic or a small register increase.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`
- latest run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- latest runtime: `24.407552 ms`
- latest NCU analysis: `runs/20260421_133418_bf16_gemm_v1_c859cd06/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.78` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.324` | Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.38` | Tensor pipe activity is only 48.38% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.49` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.49` | barrier stalls are consuming 5.49% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Swap the default fixed-shape hot-band launch from the PTX microkernel path to the existing 128x128x32 staged kernel.`
- `Keep the residual 64x384 row-band and 64x96 tail unchanged for the first measurement.`

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
