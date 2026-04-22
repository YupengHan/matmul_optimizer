# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_02`
- direction name: `Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop`
- candidate id: `diagnosis_20260421_185824:dir_02`
- base run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- primary family id: `exploit::hoist_hot_band_shared_offsets_out_of_128x128_steady_state_loops`
- planned action fingerprint: `hoist_128x128_hot_band_warp_local_shared_offsets_from_compact_ptx_base`
- selection mode: `frontier`
- source diagnosis id: `diagnosis_20260421_185824`
- round loop: `round 10/20`
- hypothesis: `Both active 128x128 hot-band kernels still carry invariant warp-local shared offset arithmetic through the K loop even though row and column warp positions are fixed for the CTA lifetime. Hoisting those offsets once per warp should shave integer address work and reduce control dilution on a surface that is already close to the branch best.`
- expected bottleneck: `Warp-local shared-pointer arithmetic and hot-loop control overhead are small but still relevant on the accepted compact PTX base.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1775-1796, src/kernels/bf16_gemm_v1.cu:1910-1925, src/kernels/bf16_gemm_v1.cu:2024-2040`
- risk: `Low. This is a bounded control-overhead cleanup and should not change tile geometry or shared-memory budgeting.`
- metrics to re-check: `median runtime, launch__registers_per_thread, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_190032_bf16_gemm_v1_9e21c98f`
- latest runtime: `24.841215 ms`
- latest NCU analysis: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `44.38` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.214` | Tensor activity (48.49%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.49` | Tensor pipe activity is only 48.49% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.96` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.96` | barrier stalls are consuming 8.96% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__registers_per_thread` `bounded_not_worse_than_current_run` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A

## Expected local changes

- `Hoist warp-local A and B shared offsets once per warp before the K loop in the active 128x128 hot-band kernels.`
- `Leave synchronization, grouped_rows, and tiling unchanged.`
- `Keep the change limited to loop-invariant address setup.`

## Delta vs previous run

- baseline run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- stall `long_scoreboard` | delta `-5.329999999999999` | trend `improved`
- stall `barrier` | delta `2.540000000000001` | trend `regressed`
- stall `mio_throttle` | delta `0.39999999999999947` | trend `regressed`
- stall `short_scoreboard` | delta `0.04999999999999982` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `6.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.38000000000000256` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.0800000000000054` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.030000000000001137` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
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

- no tracked dirty paths at prepare time
