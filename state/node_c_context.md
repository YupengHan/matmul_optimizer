# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX export/store-path scalar live state on the current 128x128 anchor`
- candidate id: `diagnosis_20260421_122308:dir_01`
- base run id: `20260421_122240_bf16_gemm_v1_b79a9bf`
- primary family id: `exploit::trim_ptx_export_address_math_in_hot_band_epilogue`
- planned action fingerprint: `trim_post_mma_export_address_live_state_after_helper_flatten_b79a9bf`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_122308`
- round loop: `round 7/100`
- hypothesis: `The helper flattening win says small PTX-local cleanup is still worth budget, but the unchanged 198-register / 16.64%-active-warps signature says the remaining pressure is no longer in the compute helper front-end. The next best bounded move is to narrow row/column-derived pointer math and per-warp export temporaries after the MMA loop so the writer path carries less scalar live state into the hot PTX epilogue.`
- expected bottleneck: `occupancy_latency_hiding_issue with tail_overhead_or_generic_path_issue concentrated in the PTX export/store path after the MMA loop`
- code locations: `src/kernels/bf16_gemm_v1.cu:804-860, src/kernels/bf16_gemm_v1.cu:1004-1065, src/kernels/bf16_gemm_v1.cu:1955-2064`
- risk: `medium`
- metrics to re-check: `median runtime, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct`
- latest run id: `20260421_122240_bf16_gemm_v1_b79a9bf`
- latest runtime: `46.021631 ms`
- latest NCU analysis: `runs/20260421_122240_bf16_gemm_v1_b79a9bf/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `198.0` | The active PTX hot-band kernel is still register-limited at 198 registers per thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Achieved occupancy is still pinned near the floor, so any store-path cleanup must buy back latency-hiding headroom.

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `42.36` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.64` | Active warps are only 16.64% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.308` | Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.64%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.38` | Tensor pipe activity is only 48.38% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.64` | Active warps are only 16.64% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.94` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.94` | barrier stalls are consuming 5.94% of active warp issue slots.

## Guardrail metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.38` | Scalar cleanup should not dilute the tensor path.
- `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.64` | The point of the cleanup is to ease latency hiding, not make it worse.
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.94` | Do not trade writer cleanup for a worse synchronization seam.

## Expected local changes

- `Push row/column-to-pointer conversion as late as possible into the final PTX writer helpers.`
- `Narrow per-warp export temporaries so they do not stay live across the whole epilogue.`
- `Keep the current grouped-row mapping, launch geometry, and shared export scratch size unchanged.`

## Delta vs previous run

- baseline run id: `20260421_114455_bf16_gemm_v1_aaf076e`
- stall `long_scoreboard` | delta `0.08999999999999986` | trend `regressed`
- stall `mio_throttle` | delta `-0.020000000000000018` | trend `improved`
- stall `barrier` | delta `0.010000000000000675` | trend `regressed`
- stall `short_scoreboard` | delta `0.009999999999999787` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-1.0199999999999996` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.28000000000000114` | trend `improved`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-0.019999999999999574` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-0.01999999999999602` | trend `regressed`

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

- `src/kernels/bf16_gemm_v1.cu`
