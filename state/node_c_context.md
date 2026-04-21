# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.
Use the structured NCU handoff as the default source of truth for local hotspots, guardrails, and delta checks.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Wait/Sync Handoff On The 128x128 Anchor`
- candidate id: `diagnosis_20260421_154619:dir_01`
- base run id: `20260421_154110_bf16_gemm_v1_afe26c16`
- primary family id: `aggressive::trim_microkernel_barriers_without_x32_shared_blowup`
- planned action fingerprint: `restore_ptx_128x128_anchor_then_batch_export_and_trim_wait_sync_without_x32_shared_growth`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_154619`
- round loop: `round 6/10`
- hypothesis: `The current 256x128 branch is no longer the right place to keep pushing: it already reached 167 regs/thread and 16.66% active warps, but it still lost badly because the synchronization regime stayed at 8.32% barrier stall and the overall kernel remained far from the cuBLASLt ceiling. cuBLAS reaches 49.39% tensor activity with only 8.33% active warps because it keeps barrier and scoreboard cost near zero. That makes the next coherent move a return to the tighter 128x128 PTX anchor plus a narrow handoff surgery that trims the wait-group and export cadence while keeping the smaller 22,016 B shared-memory footprint.`
- expected bottleneck: `Barrier cadence and export/control handoff inside the single-K 128x128 PTX microkernel, especially the seam between finishing a tile, releasing the stage with __syncthreads(), and refilling the reused buffer.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1002-1084, src/kernels/bf16_gemm_v1.cu:1983-2062, src/kernels/bf16_gemm_v1.cu:2139-2147`
- risk: `Moderate-high. This stays inside a bounded hot-band surface, but it is still PTX control-path surgery and therefore sensitive to both correctness and codegen shifts.`
- metrics to re-check: `correctness on all 3 dataset cases before trusting runtime, median runtime versus the 24.195072 ms accepted base and the 22.000000 ms cuBLAS baseline, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, gpu__time_duration.sum`
- latest run id: `20260421_154110_bf16_gemm_v1_afe26c16`
- latest runtime: `30.168575 ms`
- latest NCU analysis: `runs/20260421_154110_bf16_gemm_v1_afe26c16/ncu_analysis.json`

## Relevant hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `unknown_metric` = `None` | N/A
- `section` `Occupancy` @ `Occupancy` | `unknown_metric` = `None` | N/A

## Relevant bottleneck evidence

- `tensor_core_underutilization` | severity `43.902` | Tensor activity (36.77%) is low relative to available memory bandwidth, and active warps (16.66%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `36.77` | Tensor pipe activity is only 36.77% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- `occupancy_latency_hiding_issue` | severity `36.14` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `1.0` | Register pressure is limiting occupancy to 1 blocks per SM.
- `synchronization_barrier_issue` | severity `8.32` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.

## Guardrail metrics

- `correctness` `must_pass` from `N/A` | N/A
- `launch__shared_mem_per_block_allocated` `non_increasing` from `N/A` | N/A
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `N/A` | N/A

## Expected local changes

- `Restore the 128x128 PTX anchor launch path from the current losing 256x128 pivot.`
- `Retune the PTX wait/sync or export batching seam without reintroducing the larger x32-style shared-memory footprint.`

## Delta vs previous run

- baseline run id: `20260421_153357_bf16_gemm_v1_f1c576ee`
- stall `barrier` | delta `0.0` | trend `flat`
- stall `short_scoreboard` | delta `0.0` | trend `flat`
- stall `long_scoreboard` | delta `0.0` | trend `flat`
- stall `mio_throttle` | delta `0.0` | trend `flat`
- no structured hotspot delta is available

## Finalize recheck points

- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.

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
