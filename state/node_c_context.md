# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Repair the PTX writer row sweep while preserving the 104-register surface`
- candidate id: `diagnosis_20260421_123024:dir_01`
- base run id: `20260421_122942_bf16_gemm_v1_3eed315`
- primary family id: `exploit::repair_ptx_export_writer_correctness_on_low_register_surface`
- planned action fingerprint: `repair_missing_ptx_writer_tile_rows_2_and_3_without_giving_back_104reg_surface`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_123024`
- round loop: `round 8/100`
- hypothesis: `The new PTX export helper shape is likely directionally correct for performance, but the writer coverage is wrong. `FixedHotBandTile128x128::kWarpMmaTilesM` is 4 while the explicit `ptx_wmma_store_tile_pairs_64x64_ptx_microkernel()` sweep currently emits only TileRow 0 and 1, so half of the warp tile never reaches global memory. Restoring full tile-row coverage or an equivalent correctness-safe row sweep should recover correctness while keeping most of the new 104-register / 33.2%-active-warps surface intact.`
- expected bottleneck: `correctness recovery on the PTX export/store path first; if preserved, the new steady-state signature becomes barrier-heavy and more memory-active rather than occupancy-limited`
- code locations: `src/kernels/bf16_gemm_v1.cu:107-116, src/kernels/bf16_gemm_v1.cu:934-975, src/kernels/bf16_gemm_v1.cu:1034-1069`
- risk: `medium`
- metrics to re-check: `correctness, median runtime, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`
- latest run id: `20260421_122942_bf16_gemm_v1_3eed315`
- latest runtime: `43.250160 ms`
- latest NCU analysis: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `104.0` | The new writer shape cut the kernel to 104 registers per thread, which is worth preserving if correctness can be recovered.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `33.19` | Achieved occupancy doubled, so the repair should protect this new regime.

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `24.58` | Tensor activity (45.42%) is low relative to available memory bandwidth, and active warps (33.20%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `45.42` | Tensor pipe activity is only 45.42% of peak sustained active.
- evidence: `source_hotspot` `hotspot::section::launch_statistics::launch_statistics::registers_per_thread` | `Registers Per Thread` = `104.0` | Launch Statistics is carrying metric Registers Per Thread.
- `global_memory_bound` | severity `22.45` | Memory throughput and memory-focused sections/rules suggest the dominant kernel is being limited by global or cache movement.
- evidence: `headline_metric` `metric::gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed` | `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed` = `69.06` | Compute-memory throughput is 69.06% of peak sustained elapsed.
- `synchronization_barrier_issue` | severity `12.28` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `12.28` | barrier stalls are consuming 12.28% of active warp issue slots.

## Guardrail metrics

- `launch__occupancy_limit_registers` `non_increasing` from `4.0` | The repair should not throw away the new four-CTA register budget.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `33.2` | The main opportunity is the new active-warps regime; keep it if at all possible.
- `correctness` `must_pass` from `0.0` | This is the blocking failure that must be cleared before treating the speedup as real.

## Expected local changes

- `Restore full PTX tile-row emission for TileRow 0..3 or an equivalent correctness-safe sweep.`
- `Keep the new per-tile export helper structure instead of reverting wholesale to the old recursive writer.`
- `Preserve the current shared scratch size and late address arithmetic shape as much as correctness allows.`

## Delta vs previous run

- baseline run id: `20260421_122240_bf16_gemm_v1_b79a9bf`
- stall `barrier` | delta `6.339999999999999` | trend `regressed`
- stall `long_scoreboard` | delta `3.45` | trend `regressed`
- stall `short_scoreboard` | delta `1.79` | trend `regressed`
- stall `mio_throttle` | delta `0.05999999999999961` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-94.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `28.599999999999998` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `22.979999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `22.729999999999997` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
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

- `src/kernels/bf16_gemm_v1.cu`
