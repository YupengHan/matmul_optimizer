# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Retime the PTX barrier seam on the current correctness-safe 128x128 anchor`
- candidate id: `diagnosis_20260421_124005:dir_01`
- base run id: `20260421_123908_bf16_gemm_v1_1db08fc`
- primary family id: `aggressive::trim_microkernel_barriers_without_x32_shared_blowup`
- planned action fingerprint: `retime_wait_group_and_sync_seam_on_current_correct_1db08fc_anchor`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_124005`
- round loop: `round 10/100`
- hypothesis: `The last two writer-family iterations both landed back on the same 198-register / 16.6%-active-warps regime, so the cheapest remaining local seam on the correct anchor is the cp.async wait-group plus CTA barrier handoff. A bounded retime can target the persistent 5.95% barrier stall and 6.85% long-scoreboard stall without touching writer coverage or geometry.`
- expected bottleneck: `synchronization_barrier_issue layered on top of occupancy_latency_hiding_issue in the current correctness-safe 128x128 PTX anchor`
- code locations: `src/kernels/bf16_gemm_v1.cu:1955-2066, src/kernels/bf16_gemm_v1.cu:2023-2056, src/kernels/bf16_gemm_v1.cu:338-359`
- risk: `medium`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`
- latest run id: `20260421_123908_bf16_gemm_v1_1db08fc`
- latest runtime: `46.056448 ms`
- latest NCU analysis: `runs/20260421_123908_bf16_gemm_v1_1db08fc/ncu_analysis.json`

## Relevant hotspots

- `section` `Warp Stall Sampling` @ `Warp Stall Sampling` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.95` | Barrier remains the most actionable local stall seam on the current correct anchor.
- `section` `Warp Stall Sampling` @ `Warp Stall Sampling` | `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` = `6.85` | Any handoff retime must not simply trade barrier time for worse scoreboard pressure.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.38` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.364` | Tensor activity (48.34%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.34` | Tensor pipe activity is only 48.34% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.95` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.95` | barrier stalls are consuming 5.95% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `1.0` | This stays on the current correctness-safe anchor.
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.85` | Do not improve barrier by worsening scoreboard stalls.

## Expected local changes

- `Retune cp.async wait-group completion versus CTA-wide sync on the steady-state PTX path.`
- `Keep writer coverage and the 22016-byte shared-memory budget fixed.`
- `Do not mix barrier work with another writer sweep rewrite.`

## Delta vs previous run

- baseline run id: `20260421_123502_bf16_gemm_v1_310a824`
- stall `long_scoreboard` | delta `0.04999999999999982` | trend `regressed`
- stall `mio_throttle` | delta `-0.040000000000000036` | trend `improved`
- stall `barrier` | delta `-0.009999999999999787` | trend `improved`
- stall `short_scoreboard` | delta `0.0` | trend `flat`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `2.009999999999998` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.17` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.01999999999999602` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-0.010000000000001563` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.

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
