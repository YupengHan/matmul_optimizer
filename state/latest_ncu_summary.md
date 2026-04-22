# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- source run dir: `runs/20260421_184622_bf16_gemm_v1_d51419e6`
- status: `available`
- analysis path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_analysis.json`
- raw csv path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_metrics.csv`
- raw rep path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_details.csv`
- details page csv path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_details_page.csv`
- source page csv path: `runs/20260421_184622_bf16_gemm_v1_d51419e6/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `254.0`
- shared mem / block allocated: `30464.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `46.86`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `46.48`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `44.88`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `43.3`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `31.01`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.57`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `6.72`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `0.12`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.5`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `5.8`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `48.43` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `33.884` | Tensor activity (46.86%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.86` | Tensor pipe activity is only 46.86% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.57` | Active warps are only 16.57% of peak sustained active.
- `synchronization_barrier_issue` | severity `6.72` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `6.72` | barrier stalls are consuming 6.72% of active warp issue slots.

## Stall breakdown

- `barrier`: `6.72` | barrier stalls are consuming 6.72% of active warp issue slots.
- `mio_throttle`: `5.8` | mio throttle stalls are consuming 5.80% of active warp issue slots.
- `short_scoreboard`: `1.5` | short scoreboard stalls are consuming 1.50% of active warp issue slots.
- `long_scoreboard`: `0.12` | long scoreboard stalls are consuming 0.12% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `254.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.58` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `31.01` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `42.34` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `44.96` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `45.24` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.57` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- stall `mio_throttle`: current `5.8` vs previous `4.54` | delta `1.2599999999999998` | trend `regressed`
- stall `barrier`: current `6.72` vs previous `7.59` | delta `-0.8700000000000001` | trend `improved`
- stall `short_scoreboard`: current `1.5` vs previous `1.93` | delta `-0.42999999999999994` | trend `improved`
- stall `long_scoreboard`: current `0.12` vs previous `0.21` | delta `-0.09` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `57.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `21.460000000000004` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `2.240000000000002` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `-1.2299999999999969` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `-1.009999999999998` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-1.009999999999998` | trend `regressed`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: Occupancy is carrying metric Achieved Occupancy. (evidence: hotspot::section::occupancy::occupancy::achieved_occupancy)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Tensor activity (46.86%) is low relative to available memory bandwidth, and active warps (16.57%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `254.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.58` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `31.01` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `42.34` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `44.96` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `46.86` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.57` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `6.72` | barrier stalls are consuming 6.72% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `5.8` | mio throttle stalls are consuming 5.80% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
