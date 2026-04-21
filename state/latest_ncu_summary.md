# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_122942_bf16_gemm_v1_3eed315`
- source run dir: `runs/20260421_122942_bf16_gemm_v1_3eed315`
- status: `available`
- analysis path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_analysis.json`
- raw csv path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_metrics.csv`
- raw rep path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_details.csv`
- details page csv path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_details_page.csv`
- source page csv path: `runs/20260421_122942_bf16_gemm_v1_3eed315/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `104.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `45.42`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `45.27`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `69.06`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `31.74`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `58.39`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `33.2`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `12.28`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `10.4`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `4.04`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.76`
- `launch__occupancy_limit_registers`: `4.0`

## Primary bottlenecks

- `tensor_core_underutilization` | severity `24.58` | Tensor activity (45.42%) is low relative to available memory bandwidth, and active warps (33.20%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `45.42` | Tensor pipe activity is only 45.42% of peak sustained active.
- evidence: `source_hotspot` `hotspot::section::launch_statistics::launch_statistics::registers_per_thread` | `Registers Per Thread` = `104.0` | Launch Statistics is carrying metric Registers Per Thread.
- `global_memory_bound` | severity `22.45` | Memory throughput and memory-focused sections/rules suggest the dominant kernel is being limited by global or cache movement.
- evidence: `headline_metric` `metric::gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed` | `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed` = `69.06` | Compute-memory throughput is 69.06% of peak sustained elapsed.
- `synchronization_barrier_issue` | severity `12.28` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `12.28` | barrier stalls are consuming 12.28% of active warp issue slots.

## Stall breakdown

- `barrier`: `12.28` | barrier stalls are consuming 12.28% of active warp issue slots.
- `long_scoreboard`: `10.4` | long scoreboard stalls are consuming 10.40% of active warp issue slots.
- `short_scoreboard`: `4.04` | short scoreboard stalls are consuming 4.04% of active warp issue slots.
- `mio_throttle`: `3.76` | mio throttle stalls are consuming 3.76% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `104.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `31.76` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `33.19` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `33.33` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `45.2` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `58.11` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `69.08` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `69.36` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.

## Delta vs previous run

- baseline run id: `20260421_122240_bf16_gemm_v1_b79a9bf`
- stall `barrier`: current `12.28` vs previous `5.94` | delta `6.339999999999999` | trend `regressed`
- stall `long_scoreboard`: current `10.4` vs previous `6.95` | delta `3.45` | trend `regressed`
- stall `short_scoreboard`: current `4.04` vs previous `2.25` | delta `1.79` | trend `regressed`
- stall `mio_throttle`: current `3.76` vs previous `3.7` | delta `0.05999999999999961` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-94.0` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `28.599999999999998` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `22.979999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `22.729999999999997` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `-2.6099999999999994` | trend `regressed`

## Handoff to node_b

- finding: improved hotspot delta at Launch Statistics: improved.
- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Tensor activity (45.42%) is low relative to available memory bandwidth, and active warps (33.20%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: Memory throughput and memory-focused sections/rules suggest the dominant kernel is being limited by global or cache movement. (evidence: metric::gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `104.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `31.76` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `33.19` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `33.33` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `45.2` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `58.11` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `45.42` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `33.2` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `12.28` | barrier stalls are consuming 12.28% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `10.4` | long scoreboard stalls are consuming 10.40% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was improved in the improved bucket.
