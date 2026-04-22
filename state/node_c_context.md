# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore PTX Launch Bounds Back To 2-CTA On The Active Hot-Band Path`
- candidate id: `diagnosis_20260421_182251:dir_01`
- base run id: `20260421_182124_bf16_gemm_v1_49dfa799`
- primary family id: `register_pressure::ptx_microkernel_launch_bounds_restore`
- planned action fingerprint: `ptx_hotband_active:launch_bounds_min_blocks_3->2`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_182251`
- round loop: `round 3/20`
- hypothesis: `The current run already restored the compact PTX hot-band dispatch and preserved the 22016 B shared-memory footprint, but it still trails the accepted PTX base by about 1.50 ms while carrying the exact same 168 regs/thread. The main new lever is __launch_bounds__(128, 3), so rolling that back to 2 should recover scheduler freedom and remove the extra barrier plus short-scoreboard tax without touching grouped rows, stage depth, or the row-pair accumulator path.`
- expected bottleneck: `The explicit 3-CTA minimum is over-constraining the PTX microkernel schedule, inflating barrier and short-scoreboard even though it does not reduce the measured register footprint.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1988-1993`
- risk: `Low. This is a one-line rollback on the live PTX surface and keeps the current dispatch, shared-memory footprint, and row-pair math path intact.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`
- latest run id: `20260421_182124_bf16_gemm_v1_49dfa799`
- latest runtime: `26.306592 ms`
- latest NCU analysis: `runs/20260421_182124_bf16_gemm_v1_49dfa799/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.578` | Tensor activity (46.63%) is low relative to available memory bandwidth, and active warps (24.74%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.63` | Tensor pipe activity is only 46.63% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.74` | Active warps are only 24.74% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.73` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.73` | barrier stalls are consuming 9.73% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.26` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.74` | Active warps are only 24.74% of peak sustained active.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Retune the PTX hot-band __launch_bounds__ annotation from 3 back to 2.`
- `Leave the active PTX dispatch in place.`
- `Leave grouped rows, shared-memory stage depth, and export scratch untouched in this validation pass.`

## Delta vs previous run

- baseline run id: `20260421_175700_bf16_gemm_v1_05086a14`
- stall `short_scoreboard` | delta `0.5800000000000001` | trend `regressed`
- stall `barrier` | delta `-0.41999999999999993` | trend `improved`
- stall `mio_throttle` | delta `-0.3800000000000001` | trend `improved`
- stall `long_scoreboard` | delta `-0.08999999999999986` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `0.18999999999999773` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.120000000000001` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.03999999999999915` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.030000000000001137` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was improved in the improved bucket.
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
