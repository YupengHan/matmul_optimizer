# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_182631_bf16_gemm_v1_1f02b147`
- source run dir: `runs/20260421_182631_bf16_gemm_v1_1f02b147`
- status: `available`
- analysis path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_analysis.json`
- raw csv path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_metrics.csv`
- raw rep path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_details.csv`
- details page csv path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_details_page.csv`
- source page csv path: `runs/20260421_182631_bf16_gemm_v1_1f02b147/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `202.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.39`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.9`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.24`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `12.5`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `30.16`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.6`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `6.35`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `5.45`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.86`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.98`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `43.2` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.33` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.35` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.35` | barrier stalls are consuming 6.35% of active warp issue slots.

## Stall breakdown

- `barrier`: `6.35` | barrier stalls are consuming 6.35% of active warp issue slots.
- `long_scoreboard`: `5.45` | long scoreboard stalls are consuming 5.45% of active warp issue slots.
- `mio_throttle`: `3.98` | mio throttle stalls are consuming 3.98% of active warp issue slots.
- `short_scoreboard`: `1.86` | short scoreboard stalls are consuming 1.86% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `202.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.61` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.03` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.23` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.73` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.9` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_182124_bf16_gemm_v1_49dfa799`
- stall `short_scoreboard`: current `1.86` vs previous `7.32` | delta `-5.46` | trend `improved`
- stall `barrier`: current `6.35` vs previous `9.73` | delta `-3.380000000000001` | trend `improved`
- stall `long_scoreboard`: current `5.45` vs previous `2.17` | delta `3.2800000000000002` | trend `regressed`
- stall `mio_throttle`: current `3.98` vs previous `1.39` | delta `2.59` | trend `regressed`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `34.0` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Theoretical Occupancy` | delta `-8.329999999999998` | trend `regressed`
- hotspot delta: `regressed` `Occupancy` | `Achieved Occupancy` | delta `-8.14` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-1.6099999999999994` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `1.2899999999999991` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at Occupancy: regressed.
- finding: Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `202.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.49` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.61` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.03` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.23` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.39` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.6` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `6.35` | barrier stalls are consuming 6.35% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `5.45` | long scoreboard stalls are consuming 5.45% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was regressed in the regressed bucket.
