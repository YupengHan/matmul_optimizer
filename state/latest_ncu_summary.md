# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_193649_bf16_gemm_v1_fd009266`
- source run dir: `runs/20260421_193649_bf16_gemm_v1_fd009266`
- status: `available`
- analysis path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_analysis.json`
- raw csv path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_metrics.csv`
- raw rep path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_details.csv`
- details page csv path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_details_page.csv`
- source page csv path: `runs/20260421_193649_bf16_gemm_v1_fd009266/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel<(int)226>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `213.0`
- shared mem / block allocated: `43008.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `40.21`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `40.0`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `40.04`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `33.64`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `26.66`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.57`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `9.85`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `7.32`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.39`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `6.33`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `45.43` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `40.534` | Tensor activity (40.21%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `40.21` | Tensor pipe activity is only 40.21% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.85` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.85` | barrier stalls are consuming 9.85% of active warp issue slots.

## Stall breakdown

- `barrier`: `9.85` | barrier stalls are consuming 9.85% of active warp issue slots.
- `long_scoreboard`: `7.32` | long scoreboard stalls are consuming 7.32% of active warp issue slots.
- `mio_throttle`: `6.33` | mio throttle stalls are consuming 6.33% of active warp issue slots.
- `short_scoreboard`: `2.39` | short scoreboard stalls are consuming 2.39% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `213.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `26.65` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `35.12` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `39.98` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `40.0` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `40.22` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.

## Delta vs previous run

- baseline run id: `20260421_193214_bf16_gemm_v1_5bbcf7bf`
- stall `long_scoreboard`: current `7.32` vs previous `3.34` | delta `3.9800000000000004` | trend `regressed`
- stall `mio_throttle`: current `6.33` vs previous `4.13` | delta `2.2` | trend `regressed`
- stall `barrier`: current `9.85` vs previous `7.86` | delta `1.9899999999999993` | trend `regressed`
- stall `short_scoreboard`: current `2.39` vs previous `2.55` | delta `-0.1599999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `22.61` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `12.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-7.8700000000000045` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-6.460000000000001` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-6.299999999999997` | trend `regressed`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `0.00999999999999801` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: Occupancy is carrying metric Achieved Occupancy. (evidence: hotspot::section::occupancy::occupancy::achieved_occupancy)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (40.21%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `213.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `26.65` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `35.12` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `39.98` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `40.21` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.57` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `9.85` | barrier stalls are consuming 9.85% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `7.32` | long scoreboard stalls are consuming 7.32% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
