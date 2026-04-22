# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_194145_bf16_gemm_v1_f42c9310`
- source run dir: `runs/20260421_194145_bf16_gemm_v1_f42c9310`
- status: `available`
- analysis path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_analysis.json`
- raw csv path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_metrics.csv`
- raw rep path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_details.csv`
- details page csv path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_details_page.csv`
- source page csv path: `runs/20260421_194145_bf16_gemm_v1_f42c9310/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `201.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.28`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.85`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.3`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `12.49`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `30.49`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.57`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `7.86`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `3.33`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.55`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `4.14`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `43.03` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.464` | Tensor activity (48.28%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.28` | Tensor pipe activity is only 48.28% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- `synchronization_barrier_issue` | severity `7.86` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `7.86` | barrier stalls are consuming 7.86% of active warp issue slots.

## Stall breakdown

- `barrier`: `7.86` | barrier stalls are consuming 7.86% of active warp issue slots.
- `mio_throttle`: `4.14` | mio throttle stalls are consuming 4.14% of active warp issue slots.
- `long_scoreboard`: `3.33` | long scoreboard stalls are consuming 3.33% of active warp issue slots.
- `short_scoreboard`: `2.55` | short scoreboard stalls are consuming 2.55% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `201.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.31` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.31` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.7` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.86` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_193649_bf16_gemm_v1_fd009266`
- stall `long_scoreboard`: current `3.33` vs previous `7.32` | delta `-3.99` | trend `improved`
- stall `mio_throttle`: current `4.14` vs previous `6.33` | delta `-2.1900000000000004` | trend `improved`
- stall `barrier`: current `7.86` vs previous `9.85` | delta `-1.9899999999999993` | trend `improved`
- stall `short_scoreboard`: current `2.55` vs previous `2.39` | delta `0.1599999999999997` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-22.629999999999995` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-12.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `7.880000000000003` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `6.480000000000004` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `6.310000000000002` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at Launch Statistics: improved.
- finding: Tensor activity (48.28%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `201.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.31` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.31` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.28` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.57` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `7.86` | barrier stalls are consuming 7.86% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `4.14` | mio throttle stalls are consuming 4.14% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
