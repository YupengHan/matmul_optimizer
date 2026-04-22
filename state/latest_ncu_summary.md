# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_170056_bf16_gemm_v1_13d24542`
- source run dir: `runs/20260421_170056_bf16_gemm_v1_13d24542`
- status: `available`
- analysis path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_analysis.json`
- raw csv path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_metrics.csv`
- raw rep path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_details.csv`
- details page csv path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_details_page.csv`
- source page csv path: `runs/20260421_170056_bf16_gemm_v1_13d24542/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `241.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `37.48`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `36.98`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `58.96`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `13.23`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `24.66`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.6`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `9.8`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `4.64`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `3.19`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `15.39`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `48.4` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `43.24` | Tensor activity (37.48%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `37.48` | Tensor pipe activity is only 37.48% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.6` | Active warps are only 16.60% of peak sustained active.
- `synchronization_barrier_issue` | severity `9.8` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `9.8` | barrier stalls are consuming 9.80% of active warp issue slots.

## Stall breakdown

- `mio_throttle`: `15.39` | mio throttle stalls are consuming 15.39% of active warp issue slots.
- `barrier`: `9.8` | barrier stalls are consuming 9.80% of active warp issue slots.
- `long_scoreboard`: `4.64` | long scoreboard stalls are consuming 4.64% of active warp issue slots.
- `short_scoreboard`: `3.19` | short scoreboard stalls are consuming 3.19% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `241.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.92` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.6` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `24.67` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `36.94` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Duration` = `42.25` | GPU Speed Of Light Throughput is carrying metric Duration.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `58.91` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.

## Delta vs previous run

- baseline run id: `None`
- no structured stall delta is available

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (37.48%) is low relative to available memory bandwidth, and active warps (16.60%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow. (evidence: stall::barrier)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `241.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.92` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.6` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `24.67` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `36.94` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `37.48` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.6` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `15.39` | mio throttle stalls are consuming 15.39% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `9.8` | barrier stalls are consuming 9.80% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
