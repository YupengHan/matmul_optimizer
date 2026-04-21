# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Collapse PTX Wait-Group Handoff Without Extra Export Scratch`
- candidate id: `diagnosis_20260421_160315:dir_01`
- base run id: `20260421_160237_bf16_gemm_v1_404e8c44`
- primary family id: `sync_pipeline::ptx_microkernel_wait_sync_collapse`
- planned action fingerprint: `restore_ptx_anchor_and_collapse_wait_group_order_without_stagecount_growth`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_160315`
- round loop: `round 10/10`
- hypothesis: `The final credible near-base move is to restore the PTX 128x128 anchor and target the wait-group / refill seam directly while keeping export scratch at the single-stage footprint. The PTX anchor is still much closer to the accepted base than the non-PTX 3-CTA family, and it keeps the final round focused on synchronization quality rather than another broad family rewrite.`
- expected bottleneck: `Wait-group release, barrier cadence, and refill ordering on the PTX 128x128 anchor without extra export-scratch growth.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1983-2062, src/kernels/bf16_gemm_v1.cu:2139-2147`
- risk: `Moderate. This restores a closer-to-base family and applies one narrow retime, which is safer than reopening a broad 256x128 rewrite for the last round.`
- metrics to re-check: `correctness on all 3 dataset cases before trusting runtime, median runtime versus the 24.195072 ms accepted base, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, gpu__time_duration.sum`
- latest run id: `20260421_160237_bf16_gemm_v1_404e8c44`
- latest runtime: `25.996288 ms`
- latest NCU analysis: `runs/20260421_160237_bf16_gemm_v1_404e8c44/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `27.744` | Tensor activity (46.44%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.44` | Tensor pipe activity is only 46.44% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.16` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.16` | barrier stalls are consuming 10.16% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.23` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `non_increasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Restore the PTX 128x128 anchor launch path.`
- `Collapse the wait-group and refill seam without growing export scratch again.`

## Delta vs previous run

- baseline run id: `20260421_160001_bf16_gemm_v1_d7576a6e`
- stall `short_scoreboard` | delta `2.0300000000000002` | trend `regressed`
- stall `barrier` | delta `-1.0700000000000003` | trend `improved`
- stall `long_scoreboard` | delta `0.33000000000000007` | trend `regressed`
- stall `mio_throttle` | delta `-0.20999999999999996` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-7.3100000000000005` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-0.3500000000000014` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.240000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.11999999999999744` | trend `improved`

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was regressed in the regressed bucket.

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
