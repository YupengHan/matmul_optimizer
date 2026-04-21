# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_110929_bf16_gemm_v1_342b1c5`
- source run dir: `runs/20260421_110929_bf16_gemm_v1_342b1c5`
- status: `available`
- analysis path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_analysis.json`
- raw csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_metrics.csv`
- raw rep path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_details.csv`
- details page csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_details_page.csv`
- source page csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(256, 1, 1)`
- grid size: `(60, 25, 1)`
- registers / thread: `167.0`
- shared mem / block allocated: `42496.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `36.77`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `36.28`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `32.96`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `15.87`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `18.19`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.66`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `8.32`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `2.19`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `6.77`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `0.84`
- `launch__occupancy_limit_registers`: `1.0`

## Primary bottlenecks

- `tensor_core_underutilization` | severity `43.902` | Tensor activity (36.77%) is low relative to available memory bandwidth, and active warps (16.66%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `36.77` | Tensor pipe activity is only 36.77% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- `occupancy_latency_hiding_issue` | severity `36.14` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.66` | Active warps are only 16.66% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `1.0` | Register pressure is limiting occupancy to 1 blocks per SM.
- `synchronization_barrier_issue` | severity `8.32` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.

## Stall breakdown

- `barrier`: `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.
- `short_scoreboard`: `6.77` | short scoreboard stalls are consuming 6.77% of active warp issue slots.
- `long_scoreboard`: `2.19` | long scoreboard stalls are consuming 2.19% of active warp issue slots.
- `mio_throttle`: `0.84` | mio throttle stalls are consuming 0.84% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `167.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `15.87` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.66` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `18.19` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `32.96` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `33.4` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `36.28` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- stall `long_scoreboard`: current `2.19` vs previous `7.2` | delta `-5.01` | trend `improved`
- stall `short_scoreboard`: current `6.77` vs previous `2.16` | delta `4.609999999999999` | trend `regressed`
- stall `barrier`: current `8.32` vs previous `5.47` | delta `2.8500000000000005` | trend `regressed`
- stall `mio_throttle`: current `0.84` vs previous `3.66` | delta `-2.8200000000000003` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-33.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-13.280000000000001` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-13.170000000000002` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-11.68` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-11.560000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `3.4099999999999984` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: improved hotspot delta at Launch Statistics: improved.
- finding: Tensor activity (36.77%) is low relative to available memory bandwidth, and active warps (16.66%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `167.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `15.87` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.66` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `18.19` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `32.96` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `36.77` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.66` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `8.32` | barrier stalls are consuming 8.32% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `6.77` | short scoreboard stalls are consuming 6.77% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was regressed in the regressed bucket.
