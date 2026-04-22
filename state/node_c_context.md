# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX 64x64 Microkernel Register Footprint Back To 3-CTA Class`
- candidate id: `diagnosis_20260421_163733:dir_01`
- base run id: `20260421_160557_bf16_gemm_v1_35400d35`
- primary family id: `register_reuse::ptx_microkernel_64x64_register_budget_trim`
- planned action fingerprint: `trim_ptx_microkernel_accumulate_register_budget_to_restore_three_cta_residency`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_163733`
- round loop: `single-run`
- hypothesis: `The round-10 wait-group collapse restored the PTX anchor and fixed the barrier and short_scoreboard stalls, but it caused registers/thread to jump 168 -> 202 because the restored microkernel keeps 16 f32 accumulator fragments plus live A/B fragments across both 64x64 row pairs. By reordering ptx_wmma_accumulate_row_pair_64x64_ptx_microkernel so the two row pairs are interleaved column-by-column (Right-Left-Right-Left across RowPairBase = 0 and 2) instead of sequentially, and by reducing the simultaneous live PtxWmmaBf16Fragment count, we should be able to hold registers/thread below ~180 and restore launch__occupancy_limit_registers = 3. That directly attacks the dominant occupancy_latency_hiding_issue (severity 43.22) without touching barrier wins.`
- expected bottleneck: `Register-pressure-bound occupancy: 202 regs/thread caps SM residency at 2 CTAs, starving the long_scoreboard / mio_throttle latency hiding budget at 16.58% active warps.`
- code locations: `src/kernels/bf16_gemm_v1.cu:750-826 (ptx_wmma_accumulate_row_pair_64x64_ptx_microkernel and ptx_wmma_accumulate_tile_set_64x64_ptx_microkernel), src/kernels/bf16_gemm_v1.cu:405-408 (PtxWmmaAccTileSet64x64), src/kernels/bf16_gemm_v1.cu:1982-2095 (bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel)`
- risk: `Moderate. The microkernel ordering is performance-sensitive but fully preserves the WMMA math; correctness risk is low and register pressure can be verified with ncu launch__registers_per_thread on the first compile.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, gpu__time_duration.sum`
- latest run id: `20260421_160557_bf16_gemm_v1_35400d35`
- latest runtime: `24.691072 ms`
- latest NCU analysis: `runs/20260421_160557_bf16_gemm_v1_35400d35/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `43.22` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.366` | Tensor activity (48.37%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.37` | Tensor pipe activity is only 48.37% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.34` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.34` | barrier stalls are consuming 6.34% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A
- `launch__registers_per_thread` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Rework ptx_wmma_accumulate_row_pair_64x64_ptx_microkernel so the two row pairs are interleaved column-by-column instead of both sequentially materialized, shrinking the live A-fragment window.`
- `Confirm nvcc does not inflate fragment state by adding --maxrregcount guard only if necessary, avoiding spills to local memory.`
- `Leave wait_group_0 / wait_group_1 ordering from round 10 untouched so recovered barrier and short_scoreboard gains are preserved.`

## Delta vs previous run

- baseline run id: `20260421_160237_bf16_gemm_v1_404e8c44`
- stall `short_scoreboard` | delta `-4.88` | trend `improved`
- stall `barrier` | delta `-3.8200000000000003` | trend `improved`
- stall `long_scoreboard` | delta `3.2600000000000002` | trend `regressed`
- stall `mio_throttle` | delta `2.23` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `34.0` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Theoretical Occupancy` | delta `-8.329999999999998` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-8.18` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-1.5700000000000003` | trend `regressed`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was regressed in the regressed bucket.

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
