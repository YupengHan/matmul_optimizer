# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop`
- candidate id: `diagnosis_20260421_152228_round03_clean_2fbb368d:dir_01`
- base run id: `20260421_152228_bf16_gemm_v1_2fbb368d`
- primary family id: `exploit::hoist_hot_band_shared_offsets_out_of_128x128_steady_state_loops`
- planned action fingerprint: `hoist_128x128_hot_band_warp_local_shared_offsets_out_of_steady_state_loops`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_152228_round03_clean_2fbb368d`
- round loop: `round 3/10`
- hypothesis: `The regular 128x128 sibling already showed that a small register reduction and a cleaner consume path can recover some of the grouped-row loss. The next cheapest win is to hoist warp-local A-row and B-column shared offsets out of the hot-band steady-state loops so the active 128x128 path spends fewer issue slots on invariant pointer math while keeping the same CTA geometry, stage depth, and shared-memory footprint.`
- expected bottleneck: `Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are still diluting tensor issue on a latency-limited path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1775-1796, src/kernels/bf16_gemm_v1.cu:1910-1924, src/kernels/bf16_gemm_v1.cu:2024-2039`
- risk: `Low. The change stays inside the active 128x128 hot-band loops and should not alter CTA geometry, staging depth, or ownership.`
- metrics to re-check: `median runtime, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, launch__registers_per_thread`
- latest run id: `20260421_152228_bf16_gemm_v1_2fbb368d`
- latest runtime: `24.392608 ms`
- latest NCU analysis: `runs/20260421_152228_bf16_gemm_v1_2fbb368d/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `occupancy_latency_hiding_issue` | severity `41.98` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.324` | Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.38` | Tensor pipe activity is only 48.38% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.48` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.48` | barrier stalls are consuming 5.48% of active warp issue slots.

## Guardrail metrics

- `launch__registers_per_thread` `non_increasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Precompute warp-local A and B shared offsets once per warp before the 128x128 steady-state loops.`
- `Keep the current single-K staging and grouped_rows=4 traversal unchanged.`

## Delta vs previous run

- baseline run id: `20260421_150910_bf16_gemm_v1_7496aff2`
- stall `long_scoreboard` | delta `-0.17999999999999972` | trend `improved`
- stall `mio_throttle` | delta `-0.16000000000000014` | trend `improved`
- stall `barrier` | delta `0.15000000000000036` | trend `regressed`
- stall `short_scoreboard` | delta `0.07000000000000028` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-4.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `2.7300000000000004` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.8699999999999974` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.04999999999999716` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
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

- no tracked dirty paths at prepare time
