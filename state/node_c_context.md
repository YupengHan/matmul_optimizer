# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Split The Final 3-Stage PTX Drain Out Of The Late Steady-State Loop`
- candidate id: `diagnosis_20260421_184151:dir_01`
- base run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- primary family id: `sync_pipeline::ptx_microkernel_epilogue_drain_split`
- planned action fingerprint: `ptx_microkernel:pull_final_wait_sync_out_of_steady_state_loop_after_3stage_pg2s`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_184151`
- round loop: `round 6/20`
- hypothesis: `The 3-stage ring already solved the long_scoreboard problem, but the kernel still pays a full CTA sync on each late handoff while draining a larger in-flight shared-memory footprint. Pulling the no-refill drain into a narrower late path should keep the 3-stage latency win while trimming the extra barrier and mio_throttle tax that made both 4948b8ea and c03bcd3a lose.`
- expected bottleneck: `Late-drain synchronization is now the clearest remaining local tax on the 3-stage PTX surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2055-2090`
- risk: `Moderate. This stays on the current PTX family and does not reopen tiling or dispatch, but it touches delicate wait_group drain logic and can still break correctness if mistimed.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__shared_mem_per_block_allocated`
- latest run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- latest runtime: `25.755136 ms`
- latest NCU analysis: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `mio_throttle` @ `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.21` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.668` | Tensor activity (48.06%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.06` | Tensor pipe activity is only 48.06% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `7.59` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `7.59` | barrier stalls are consuming 7.59% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `bounded_not_worse_than_current_run` from `N/A` | N/A

## Expected local changes

- `Split the late no-refill drain from the current 3-stage steady-state path.`
- `Keep stage count at 3 and leave grouped_rows unchanged in the first pass.`
- `Do not touch launch bounds or the accumulator schedule while testing the drain seam.`

## Delta vs previous run

- baseline run id: `20260421_183233_bf16_gemm_v1_4948b8ea`
- stall `mio_throttle` | delta `-0.03000000000000025` | trend `improved`
- stall `short_scoreboard` | delta `0.030000000000000027` | trend `regressed`
- stall `long_scoreboard` | delta `-0.010000000000000009` | trend `improved`
- stall `barrier` | delta `-0.009999999999999787` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `8.44` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.740000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.03999999999999915` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `0.010000000000001563` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.

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
