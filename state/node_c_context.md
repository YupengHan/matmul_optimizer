# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Clean Compact PTX Anchor After The Failed Three-CTA Probe`
- candidate id: `diagnosis_20260421_194853:dir_01`
- base run id: `20260421_194813_bf16_gemm_v1_257c9662`
- primary family id: `restore_base::accepted_compact_ptx_cadence_after_failed_launch_bounds_probe`
- planned action fingerprint: `restore_clean_compact_ptx_anchor_launch_bounds_3->2_after_round19_loss`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_194853`
- round loop: `round 20/20`
- hypothesis: `The round-19 loss shows that forcing 3-CTA residency hurts the compact PTX issue schedule more than it helps latency hiding. Restoring `__launch_bounds__(128, 2)` should return the branch to the clean compact anchor and recover the 1.39 ms regression.`
- expected bottleneck: `The immediate problem is a failed register-budget probe, not an unresolved algorithmic bottleneck.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2012`
- risk: `Low. This is a one-line rollback to the known-good clean anchor configuration.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_194813_bf16_gemm_v1_257c9662`
- latest runtime: `26.079727 ms`
- latest NCU analysis: `runs/20260421_194813_bf16_gemm_v1_257c9662/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `short_scoreboard` @ `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.634` | Tensor activity (46.55%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.55` | Tensor pipe activity is only 46.55% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.64` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.64` | barrier stalls are consuming 9.64% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.23` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__occupancy_limit_registers` `return_to_2cta_anchor_class` from `N/A` | N/A
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Reset the compact PTX microkernel launch-bounds annotation from 3 back to 2.`
- `Leave grouped_rows=4, the clean wait/sync cadence, dispatch routing, and stage depth unchanged.`

## Delta vs previous run

- baseline run id: `20260421_194414_bf16_gemm_v1_ac1299d7`
- stall `short_scoreboard` | delta `3.76` | trend `regressed`
- stall `long_scoreboard` | delta `-2.83` | trend `improved`
- stall `mio_throttle` | delta `-2.21` | trend `improved`
- stall `barrier` | delta `1.5099999999999998` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-33.0` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Theoretical Occupancy` | delta `8.329999999999998` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `8.14` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.6600000000000001` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was improved in the improved bucket.

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
