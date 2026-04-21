# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_142317_bf16_gemm_v1_5ea07e35`
- source run dir: `runs/20260421_142317_bf16_gemm_v1_5ea07e35`
- status: `available`
- analysis path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_analysis.json`
- raw csv path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_metrics.csv`
- raw rep path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_details.csv`
- details page csv path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_details_page.csv`
- source page csv path: `runs/20260421_142317_bf16_gemm_v1_5ea07e35/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128x32_kernel<(int)226>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `212.0`
- shared mem / block allocated: `43008.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `40.12`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `39.72`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `40.73`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `15.27`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `26.45`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.58`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `10.09`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `5.57`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.7`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `4.84`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `45.22` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `40.616` | Tensor activity (40.12%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `40.12` | Tensor pipe activity is only 40.12% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.09` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.09` | barrier stalls are consuming 10.09% of active warp issue slots.

## Stall breakdown

- `barrier`: `10.09` | barrier stalls are consuming 10.09% of active warp issue slots.
- `long_scoreboard`: `5.57` | long scoreboard stalls are consuming 5.57% of active warp issue slots.
- `mio_throttle`: `4.84` | mio throttle stalls are consuming 4.84% of active warp issue slots.
- `short_scoreboard`: `2.7` | short scoreboard stalls are consuming 2.70% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `212.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.58` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `26.48` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `39.68` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `40.57` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `41.04` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.

## Delta vs previous run

- baseline run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- stall `barrier`: current `10.09` vs previous `5.49` | delta `4.6` | trend `regressed`
- stall `long_scoreboard`: current `5.57` vs previous `7.19` | delta `-1.62` | trend `improved`
- stall `mio_throttle`: current `4.84` vs previous `3.64` | delta `1.1999999999999997` | trend `regressed`
- stall `short_scoreboard`: current `2.7` vs previous `2.16` | delta `0.54` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `12.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-8.160000000000004` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-5.630000000000003` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-5.57` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `2.08` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (40.12%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `212.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.58` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.56` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `26.48` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `39.68` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `40.12` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.58` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `10.09` | barrier stalls are consuming 10.09% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `5.57` | long scoreboard stalls are consuming 5.57% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was regressed in the regressed bucket.
