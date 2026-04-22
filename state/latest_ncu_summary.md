# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_185050_bf16_gemm_v1_434ded2a`
- source run dir: `runs/20260421_185050_bf16_gemm_v1_434ded2a`
- status: `available`
- analysis path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_analysis.json`
- raw csv path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_metrics.csv`
- raw rep path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_details.csv`
- details page csv path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_details_page.csv`
- source page csv path: `runs/20260421_185050_bf16_gemm_v1_434ded2a/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `202.0`
- shared mem / block allocated: `22016.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.39`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.91`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.23`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `21.0`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `29.03`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.59`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `5.76`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `6.1`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.83`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.81`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `43.21` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.338` | Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.39` | Tensor pipe activity is only 48.39% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `5.76` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `5.76` | barrier stalls are consuming 5.76% of active warp issue slots.

## Stall breakdown

- `long_scoreboard`: `6.1` | long scoreboard stalls are consuming 6.10% of active warp issue slots.
- `barrier`: `5.76` | barrier stalls are consuming 5.76% of active warp issue slots.
- `mio_throttle`: `3.81` | mio throttle stalls are consuming 3.81% of active warp issue slots.
- `short_scoreboard`: `1.83` | short scoreboard stalls are consuming 1.83% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `202.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.59` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `21.01` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.05` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.22` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.67` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.9` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_184622_bf16_gemm_v1_d51419e6`
- stall `long_scoreboard`: current `6.1` vs previous `0.12` | delta `5.9799999999999995` | trend `regressed`
- stall `mio_throttle`: current `3.81` vs previous `5.8` | delta `-1.9899999999999998` | trend `improved`
- stall `barrier`: current `5.76` vs previous `6.72` | delta `-0.96` | trend `improved`
- stall `short_scoreboard`: current `1.83` vs previous `1.5` | delta `0.33000000000000007` | trend `regressed`
- hotspot delta: `improved` `Launch Statistics` | `Registers Per Thread` | delta `-52.0` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `-21.330000000000002` | trend `regressed`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-1.9600000000000009` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `1.4299999999999997` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` | delta `1.3299999999999983` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `1.259999999999998` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: Occupancy is carrying metric Achieved Occupancy. (evidence: hotspot::section::occupancy::occupancy::achieved_occupancy)
- finding: improved hotspot delta at Launch Statistics: improved.
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: Tensor activity (48.39%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `202.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.59` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `21.01` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `29.05` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `46.22` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.39` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.59` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct` `non_increasing` from `6.1` | long scoreboard stalls are consuming 6.10% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `5.76` | barrier stalls are consuming 5.76% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was regressed in the regressed bucket.
