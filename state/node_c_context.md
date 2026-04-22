# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Compact Two-Stage PTX Wait-Sync Cadence On The 22016B Shared Surface`
- candidate id: `diagnosis_20260421_185824:dir_01`
- base run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- primary family id: `sync_pipeline::trim_microkernel_barriers_without_shared_blowup`
- planned action fingerprint: `compact_two_stage_ptx_hotband:trim_wait_sync_cadence_from_24p697_frontier_base`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_185824`
- round loop: `round 9/20`
- hypothesis: `Now that grouped_rows and register pressure are back on the compact winning surface, the most actionable remaining tax is CTA handoff cadence itself. A narrow retime of wait_group and __syncthreads placement on the 22,016 B PTX loop should reduce barrier without reopening the stage-count or shared-memory regressions from the failed round-6 branch.`
- expected bottleneck: `Barrier and CTA handoff overhead are the clearest remaining local bottlenecks on the accepted compact PTX base.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2050-2096`
- risk: `Moderate. This stays entirely on the compact two-stage PTX loop, but it still touches fragile synchronization semantics.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__shared_mem_per_block_allocated, launch__registers_per_thread`
- latest run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- latest runtime: `24.697857 ms`
- latest NCU analysis: `runs/20260421_185710_bf16_gemm_v1_823cbff4/ncu_analysis.json`

## Relevant hotspots

- `stall_breakdown` `barrier` @ `smsp__warp_issue_stalled_barrier_per_warp_active.pct` | `unknown_metric` = `None` | N/A
- `stall_breakdown` `long_scoreboard` @ `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.22` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.366` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.42` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.42` | barrier stalls are consuming 6.42% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `non_increasing_vs_current_run` from `N/A` | N/A
- `launch__registers_per_thread` `bounded_not_worse_than_current_run` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing_vs_current_run` from `N/A` | N/A

## Expected local changes

- `Retune wait_group and __syncthreads placement inside the compact two-stage PTX hot-band loop.`
- `Keep stage depth at 2 and shared memory at 22,016 B.`
- `Do not change grouped_rows or launch geometry in the first pass.`

## Delta vs previous run

- baseline run id: `20260421_185050_bf16_gemm_v1_434ded2a`
- stall `barrier` | delta `0.6600000000000001` | trend `regressed`
- stall `long_scoreboard` | delta `-0.5800000000000001` | trend `improved`
- stall `mio_throttle` | delta `0.18000000000000016` | trend `regressed`
- stall `short_scoreboard` | delta `0.040000000000000036` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-8.510000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.9600000000000009` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.05999999999999517` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.020000000000003126` | trend `improved`

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
