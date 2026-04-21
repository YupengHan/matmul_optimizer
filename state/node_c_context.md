# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Grouped-Row 128x128 Sibling Export Scratch To Single Stage`
- candidate id: `diagnosis_20260421_155620:dir_01`
- base run id: `20260421_155533_bf16_gemm_v1_83acaae4`
- primary family id: `shared_memory::trim_grouped_row_non_ptx_export_scratch_to_single_stage`
- planned action fingerprint: `keep_non_ptx_three_cta_surface_but_restore_ptx_style_single_stage_export_scratch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_155620`
- round loop: `round 8/10`
- hypothesis: `Round 7 was not a clean test of 3-CTA residency on the non-PTX sibling because the source still carried a two-stage export scratch lifetime from round 6. That inflated the sibling to 26,112 B shared memory per block while barrier rose to 11.31%. The cleanest next move is to keep the same grouped-row non-PTX 128x128 sibling surface and the same 3-CTA residency target, but trim export scratch back to a single stage so the loop can see whether the barrier tax came from occupancy itself or from the coupled scratch growth.`
- expected bottleneck: `Shared export lifetime and barrier tax on the grouped-row non-PTX 128x128 sibling, currently confounded with the 3-CTA residency probe.`
- code locations: `src/kernels/bf16_gemm_v1.cu:135-145, src/kernels/bf16_gemm_v1.cu:1869-1981`
- risk: `Low-moderate. This is a narrow rollback of one coupled shared/export choice on an otherwise already-correct surface.`
- metrics to re-check: `correctness on all 3 dataset cases before trusting runtime, median runtime versus the 24.195072 ms accepted base, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_barrier_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, gpu__time_duration.sum`
- latest run id: `20260421_155533_bf16_gemm_v1_83acaae4`
- latest runtime: `26.541056 ms`
- latest NCU analysis: `runs/20260421_155533_bf16_gemm_v1_83acaae4/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.394` | Tensor activity (46.83%) is low relative to available memory bandwidth, and active warps (24.72%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.83` | Tensor pipe activity is only 46.83% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.72` | Active warps are only 24.72% of peak sustained active.
- `synchronization_barrier_issue` | severity `11.31` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `11.31` | barrier stalls are consuming 11.31% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.28` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.72` | Active warps are only 24.72% of peak sustained active.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `non_increasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Keep the grouped-row non-PTX 128x128 sibling launch path and 3-CTA residency target.`
- `Trim export scratch from the current two-stage lifetime back to the PTX-style single stage.`

## Delta vs previous run

- baseline run id: `20260421_155210_bf16_gemm_v1_9cac32cb`
- stall `barrier` | delta `5.7` | trend `regressed`
- stall `long_scoreboard` | delta `-5.16` | trend `improved`
- stall `short_scoreboard` | delta `2.5300000000000002` | trend `regressed`
- stall `mio_throttle` | delta `-1.7199999999999998` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-32.0` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Theoretical Occupancy` | delta `8.329999999999998` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `8.100000000000001` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `7.989999999999998` | trend `improved`

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

- no tracked dirty paths at prepare time
