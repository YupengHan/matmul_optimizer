# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_160001_bf16_gemm_v1_d7576a6e`
- source run dir: `runs/20260421_160001_bf16_gemm_v1_d7576a6e`
- status: `available`
- analysis path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_analysis.json`
- raw csv path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_metrics.csv`
- raw rep path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_details.csv`
- details page csv path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_details_page.csv`
- source page csv path: `runs/20260421_160001_bf16_gemm_v1_d7576a6e/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `168.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `46.89`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `46.79`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `47.39`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `21.61`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `31.18`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `24.72`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `11.23`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `1.94`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `4.71`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `1.98`
- `launch__occupancy_limit_registers`: `3.0`

## Primary bottlenecks

- `tensor_core_underutilization` | severity `27.334` | Tensor activity (46.89%) is low relative to available memory bandwidth, and active warps (24.72%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.89` | Tensor pipe activity is only 46.89% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.72` | Active warps are only 24.72% of peak sustained active.
- `synchronization_barrier_issue` | severity `11.23` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `11.23` | barrier stalls are consuming 11.23% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.28` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.72` | Active warps are only 24.72% of peak sustained active.

## Stall breakdown

- `barrier`: `11.23` | barrier stalls are consuming 11.23% of active warp issue slots.
- `short_scoreboard`: `4.71` | short scoreboard stalls are consuming 4.71% of active warp issue slots.
- `mio_throttle`: `1.98` | mio throttle stalls are consuming 1.98% of active warp issue slots.
- `long_scoreboard`: `1.94` | long scoreboard stalls are consuming 1.94% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `21.37` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.72` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `31.19` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.78` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `47.43` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `47.53` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.

## Delta vs previous run

- baseline run id: `20260421_155533_bf16_gemm_v1_83acaae4`
- stall `short_scoreboard`: current `4.71` vs previous `4.62` | delta `0.08999999999999986` | trend `regressed`
- stall `barrier`: current `11.23` vs previous `11.31` | delta `-0.08000000000000007` | trend `improved`
- stall `mio_throttle`: current `1.98` vs previous `2.06` | delta `-0.08000000000000007` | trend `improved`
- stall `long_scoreboard`: current `1.94` vs previous `1.93` | delta `0.010000000000000009` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.9200000000000017` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `0.05000000000000426` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.05000000000000426` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `0.0400000000000027` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: Tensor activity (46.89%) is low relative to available memory bandwidth, and active warps (24.72%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow. (evidence: stall::barrier)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `21.37` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.72` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `31.19` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.78` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `46.89` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `24.72` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `11.23` | barrier stalls are consuming 11.23% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `4.71` | short scoreboard stalls are consuming 4.71% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | Previous delta was improved in the improved bucket.
