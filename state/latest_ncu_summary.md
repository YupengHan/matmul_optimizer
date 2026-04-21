# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_123502_bf16_gemm_v1_310a824`
- source run dir: `runs/20260421_123502_bf16_gemm_v1_310a824`
- status: `available`
- analysis path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_analysis.json`
- raw csv path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_metrics.csv`
- raw rep path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_details.csv`
- details page csv path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_details_page.csv`
- source page csv path: `runs/20260421_123502_bf16_gemm_v1_310a824/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `198.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.34`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.83`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.12`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `15.36`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `29.47`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.63`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `5.96`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `6.8`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.25`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.77`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `42.37` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.356` | Tensor activity (48.34%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.34` | Tensor pipe activity is only 48.34% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.96` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.96` | barrier stalls are consuming 5.96% of active warp issue slots.

## Stall breakdown

- `long_scoreboard`: `6.8` | long scoreboard stalls are consuming 6.80% of active warp issue slots.
- `barrier`: `5.96` | barrier stalls are consuming 5.96% of active warp issue slots.
- `mio_throttle`: `3.77` | mio throttle stalls are consuming 3.77% of active warp issue slots.
- `short_scoreboard`: `2.25` | short scoreboard stalls are consuming 2.25% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `198.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `13.42` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `27.69` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.1` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.61` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.82` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_122942_bf16_gemm_v1_3eed315`
- stall `barrier`: current `5.96` vs previous `12.28` | delta `-6.319999999999999` | trend `improved`
- stall `long_scoreboard`: current `6.8` vs previous `10.4` | delta `-3.6000000000000005` | trend `improved`
- stall `short_scoreboard`: current `2.25` vs previous `4.04` | delta `-1.79` | trend `improved`
- stall `mio_throttle`: current `3.77` vs previous `3.76` | delta `0.010000000000000231` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `94.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-30.419999999999998` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-22.979999999999997` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-22.75` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `2.6199999999999974` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (48.34%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `198.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `13.42` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `27.69` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.1` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.34` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.8` | long scoreboard stalls are consuming 6.80% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.96` | barrier stalls are consuming 5.96% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
