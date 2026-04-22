# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_175700_bf16_gemm_v1_05086a14`
- source run dir: `runs/20260421_175700_bf16_gemm_v1_05086a14`
- status: `available`
- analysis path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_analysis.json`
- raw csv path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_metrics.csv`
- raw rep path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_details.csv`
- details page csv path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_details_page.csv`
- source page csv path: `runs/20260421_175700_bf16_gemm_v1_05086a14/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `168.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `46.46`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `46.42`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `47.54`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `14.06`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `30.95`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `24.77`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `10.15`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `2.26`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `6.74`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `1.77`
- `launch__occupancy_limit_registers`: `3.0`

## Primary bottlenecks

- `tensor_core_underutilization` | severity `27.724` | Tensor activity (46.46%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `46.46` | Tensor pipe activity is only 46.46% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.
- `synchronization_barrier_issue` | severity `10.15` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `10.15` | barrier stalls are consuming 10.15% of active warp issue slots.
- `occupancy_latency_hiding_issue` | severity `8.23` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `24.77` | Active warps are only 24.77% of peak sustained active.

## Stall breakdown

- `barrier`: `10.15` | barrier stalls are consuming 10.15% of active warp issue slots.
- `short_scoreboard`: `6.74` | short scoreboard stalls are consuming 6.74% of active warp issue slots.
- `long_scoreboard`: `2.26` | long scoreboard stalls are consuming 2.26% of active warp issue slots.
- `mio_throttle`: `1.77` | mio throttle stalls are consuming 1.77% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.06` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.77` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.95` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.42` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `47.54` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `47.58` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.

## Delta vs previous run

- baseline run id: `20260421_172601_bf16_gemm_v1_117cd3e7`
- stall `short_scoreboard`: current `6.74` vs previous `1.86` | delta `4.88` | trend `regressed`
- stall `barrier`: current `10.15` vs previous `6.39` | delta `3.7600000000000007` | trend `regressed`
- stall `long_scoreboard`: current `2.26` vs previous `5.53` | delta `-3.2700000000000005` | trend `improved`
- stall `mio_throttle`: current `1.77` vs previous `3.98` | delta `-2.21` | trend `improved`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-34.0` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Theoretical Occupancy` | delta `8.329999999999998` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `8.190000000000001` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `1.5500000000000007` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-1.4799999999999969` | trend `regressed`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: improved hotspot delta at Launch Statistics: improved.
- finding: improved hotspot delta at Occupancy: improved.
- finding: Tensor activity (46.46%) is low relative to available memory bandwidth, and active warps (24.77%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow. (evidence: stall::barrier)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `168.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.06` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `24.77` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `25.0` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `30.95` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `46.42` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `46.46` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `24.77` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `10.15` | barrier stalls are consuming 10.15% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct` `non_increasing` from `6.74` | short scoreboard stalls are consuming 6.74% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Previous delta was improved in the improved bucket.
