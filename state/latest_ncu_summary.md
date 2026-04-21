# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_155210_bf16_gemm_v1_9cac32cb`
- source run dir: `runs/20260421_155210_bf16_gemm_v1_9cac32cb`
- status: `available`
- analysis path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_analysis.json`
- raw csv path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_metrics.csv`
- raw rep path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_details.csv`
- details page csv path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_details_page.csv`
- source page csv path: `runs/20260421_155210_bf16_gemm_v1_9cac32cb/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `200.0`
- shared mem / block allocated: `26112.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.38`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.82`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.11`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `12.45`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `30.08`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.63`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `5.61`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `7.09`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.09`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.78`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `42.77` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.316` | Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.38` | Tensor pipe activity is only 48.38% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.63` | Active warps are only 16.63% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.61` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.61` | barrier stalls are consuming 5.61% of active warp issue slots.

## Stall breakdown

- `long_scoreboard`: `7.09` | long scoreboard stalls are consuming 7.09% of active warp issue slots.
- `barrier`: `5.61` | barrier stalls are consuming 5.61% of active warp issue slots.
- `mio_throttle`: `3.78` | mio throttle stalls are consuming 3.78% of active warp issue slots.
- `short_scoreboard`: `2.09` | short scoreboard stalls are consuming 2.09% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `200.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.46` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.61` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.89` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.11` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.63` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.83` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_154110_bf16_gemm_v1_afe26c16`
- stall `long_scoreboard`: current `7.09` vs previous `2.19` | delta `4.9` | trend `regressed`
- stall `short_scoreboard`: current `2.09` vs previous `6.77` | delta `-4.68` | trend `improved`
- stall `mio_throttle`: current `3.78` vs previous `0.84` | delta `2.94` | trend `regressed`
- stall `barrier`: current `5.61` vs previous `8.32` | delta `-2.71` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `33.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `13.220000000000006` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `13.149999999999999` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `11.7` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `11.549999999999997` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-3.4099999999999984` | trend `regressed`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Tensor activity (48.38%) is low relative to available memory bandwidth, and active warps (16.63%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `200.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `12.46` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.61` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.89` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.11` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.38` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.63` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `7.09` | long scoreboard stalls are consuming 7.09% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.61` | barrier stalls are consuming 5.61% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | Previous delta was improved in the improved bucket.
