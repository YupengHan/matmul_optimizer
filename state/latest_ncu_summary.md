# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_190032_bf16_gemm_v1_9e21c98f`
- source run dir: `runs/20260421_190032_bf16_gemm_v1_9e21c98f`
- status: `available`
- analysis path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_analysis.json`
- raw csv path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_metrics.csv`
- raw rep path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_details.csv`
- details page csv path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_details_page.csv`
- source page csv path: `runs/20260421_190032_bf16_gemm_v1_9e21c98f/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `208.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.49`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.92`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.26`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `12.52`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `29.83`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.62`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `8.96`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `0.19`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.92`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `4.39`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `44.38` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.214` | Tensor activity (48.49%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.49` | Tensor pipe activity is only 48.49% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.62` | Active warps are only 16.62% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.96` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.96` | barrier stalls are consuming 8.96% of active warp issue slots.

## Stall breakdown

- `barrier`: `8.96` | barrier stalls are consuming 8.96% of active warp issue slots.
- `mio_throttle`: `4.39` | mio throttle stalls are consuming 4.39% of active warp issue slots.
- `short_scoreboard`: `1.92` | short scoreboard stalls are consuming 1.92% of active warp issue slots.
- `long_scoreboard`: `0.19` | long scoreboard stalls are consuming 0.19% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `208.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.63` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.27` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.81` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.93` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_185710_bf16_gemm_v1_823cbff4`
- stall `long_scoreboard`: current `0.19` vs previous `5.52` | delta `-5.329999999999999` | trend `improved`
- stall `barrier`: current `8.96` vs previous `6.42` | delta `2.540000000000001` | trend `regressed`
- stall `mio_throttle`: current `4.39` vs previous `3.99` | delta `0.39999999999999947` | trend `regressed`
- stall `short_scoreboard`: current `1.92` vs previous `1.87` | delta `0.04999999999999982` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `6.0` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.38000000000000256` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.0800000000000054` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.030000000000001137` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `0.030000000000001137` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `0.019999999999999574` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (48.49%) is low relative to available memory bandwidth, and active warps (16.62%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `208.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.62` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.63` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.27` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.49` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.62` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `8.96` | barrier stalls are consuming 8.96% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `4.39` | mio throttle stalls are consuming 4.39% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
