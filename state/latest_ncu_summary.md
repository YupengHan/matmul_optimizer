# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_124420_bf16_gemm_v1_fc400df`
- source run dir: `runs/20260421_124420_bf16_gemm_v1_fc400df`
- status: `available`
- analysis path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_analysis.json`
- raw csv path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_metrics.csv`
- raw rep path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_details.csv`
- details page csv path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_details_page.csv`
- source page csv path: `runs/20260421_124420_bf16_gemm_v1_fc400df/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `208.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.33`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.95`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.52`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `15.34`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `29.33`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.58`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `8.09`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `0.81`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.55`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `5.0`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `44.42` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.406` | Tensor activity (48.33%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.33` | Tensor pipe activity is only 48.33% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.58` | Active warps are only 16.58% of peak sustained active.
- `synchronization_barrier_issue` | severity `8.09` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `8.09` | barrier stalls are consuming 8.09% of active warp issue slots.

## Stall breakdown

- `barrier`: `8.09` | barrier stalls are consuming 8.09% of active warp issue slots.
- `mio_throttle`: `5.0` | mio throttle stalls are consuming 5.00% of active warp issue slots.
- `short_scoreboard`: `1.55` | short scoreboard stalls are consuming 1.55% of active warp issue slots.
- `long_scoreboard`: `0.81` | long scoreboard stalls are consuming 0.81% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `208.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.89` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.59` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.44` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.53` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.96` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.95` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_123908_bf16_gemm_v1_1db08fc`
- stall `long_scoreboard`: current `0.81` vs previous `6.85` | delta `-6.039999999999999` | trend `improved`
- stall `barrier`: current `8.09` vs previous `5.95` | delta `2.1399999999999997` | trend `regressed`
- stall `mio_throttle`: current `5.0` vs previous `3.73` | delta `1.27` | trend `regressed`
- stall `short_scoreboard`: current `1.55` vs previous `2.25` | delta `-0.7` | trend `improved`
- hotspot delta: `regressed` `Launch Statistics` | `Registers Per Thread` | delta `10.0` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.4299999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.36999999999999744` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `0.3000000000000007` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.259999999999998` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `0.14000000000000057` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: GPU Speed Of Light Throughput is carrying metric DRAM Throughput. (evidence: hotspot::section::gpu_speed_of_light_throughput::gpu_speed_of_light_throughput::dram_throughput)
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at Launch Statistics: regressed.
- finding: Tensor activity (48.33%) is low relative to available memory bandwidth, and active warps (16.58%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `208.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `14.89` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.59` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.44` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.53` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.33` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.58` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `8.09` | barrier stalls are consuming 8.09% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `5.0` | mio throttle stalls are consuming 5.00% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was regressed in the regressed bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` | Previous delta was improved in the improved bucket.
