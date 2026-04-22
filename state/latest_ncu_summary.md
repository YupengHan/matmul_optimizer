# Latest Nsight Compute summary

- schema version: `2`
- source run id: `20260421_183606_bf16_gemm_v1_c03bcd3a`
- source run dir: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a`
- status: `available`
- analysis path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_analysis.json`
- raw csv path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_metrics.csv`
- raw rep path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_profile.ncu-rep`
- imported raw csv path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_import_raw.csv`
- legacy import-raw alias path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_details.csv`
- details page csv path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_details_page.csv`
- source page csv path: `runs/20260421_183606_bf16_gemm_v1_c03bcd3a/ncu_source.csv`

## Launch / kernel metadata

- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `197.0`
- shared mem / block allocated: `30464.0`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.06`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.58`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `45.97`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `20.9`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `28.81`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.59`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `7.59`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `0.21`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `1.93`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `4.54`
- `launch__occupancy_limit_registers`: `2.0`

## Primary bottlenecks

- `occupancy_latency_hiding_issue` | severity `42.21` | Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- evidence: `headline_metric` `metric::launch__occupancy_limit_registers` | `launch__occupancy_limit_registers` = `2.0` | Register pressure is limiting occupancy to 2 blocks per SM.
- `tensor_core_underutilization` | severity `32.668` | Tensor activity (48.06%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency.
- evidence: `headline_metric` `metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` | `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` = `48.06` | Tensor pipe activity is only 48.06% of peak sustained active.
- evidence: `headline_metric` `metric::sm__warps_active.avg.pct_of_peak_sustained_active` | `sm__warps_active.avg.pct_of_peak_sustained_active` = `16.59` | Active warps are only 16.59% of peak sustained active.
- `synchronization_barrier_issue` | severity `7.59` | Barrier or synchronization evidence suggests CTA-level handoff overhead is interrupting the steady-state issue flow.
- evidence: `stall_breakdown` `stall::barrier` | `smsp__warp_issue_stalled_barrier_per_warp_active.pct` = `7.59` | barrier stalls are consuming 7.59% of active warp issue slots.

## Stall breakdown

- `barrier`: `7.59` | barrier stalls are consuming 7.59% of active warp issue slots.
- `mio_throttle`: `4.54` | mio throttle stalls are consuming 4.54% of active warp issue slots.
- `short_scoreboard`: `1.93` | short scoreboard stalls are consuming 1.93% of active warp issue slots.
- `long_scoreboard`: `0.21` | long scoreboard stalls are consuming 0.21% of active warp issue slots.

## Top hotspots

- `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `197.0` | Launch Statistics is carrying metric Registers Per Thread.
- `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.6` | Occupancy is carrying metric Achieved Occupancy.
- `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `20.88` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `28.77` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `45.97` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` = `46.47` | GPU Speed Of Light Throughput is carrying metric L1/TEX Cache Throughput.
- `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Compute (SM) Throughput` = `47.58` | GPU Speed Of Light Throughput is carrying metric Compute (SM) Throughput.

## Delta vs previous run

- baseline run id: `20260421_183233_bf16_gemm_v1_4948b8ea`
- stall `mio_throttle`: current `4.54` vs previous `4.57` | delta `-0.03000000000000025` | trend `improved`
- stall `short_scoreboard`: current `1.93` vs previous `1.9` | delta `0.030000000000000027` | trend `regressed`
- stall `long_scoreboard`: current `0.21` vs previous `0.22` | delta `-0.010000000000000009` | trend `improved`
- stall `barrier`: current `7.59` vs previous `7.6` | delta `-0.009999999999999787` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `DRAM Throughput` | delta `8.44` | trend `improved`
- hotspot delta: `regressed` `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | delta `-0.740000000000002` | trend `regressed`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `L1/TEX Cache Throughput` | delta `0.03999999999999915` | trend `improved`
- hotspot delta: `improved` `Occupancy` | `Achieved Occupancy` | delta `0.010000000000001563` | trend `improved`
- hotspot delta: `improved` `GPU Speed Of Light Throughput` | `Memory Throughput` | delta `0.00999999999999801` | trend `improved`

## Handoff to node_b

- finding: Launch Statistics is carrying metric Registers Per Thread. (evidence: hotspot::section::launch_statistics::launch_statistics::registers_per_thread)
- finding: Occupancy is carrying metric Achieved Occupancy. (evidence: hotspot::section::occupancy::occupancy::achieved_occupancy)
- finding: Low active-warps and occupancy limits point to a latency-hiding problem rather than pure bandwidth saturation. (evidence: metric::sm__warps_active.avg.pct_of_peak_sustained_active)
- finding: improved hotspot delta at GPU Speed Of Light Throughput: improved.
- finding: Tensor activity (48.06%) is low relative to available memory bandwidth, and active warps (16.59%) are not hiding latency. (evidence: metric::sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active)
- finding: regressed hotspot delta at GPU Speed Of Light Throughput: regressed.
- investigate `section` `Launch Statistics` @ `Launch Statistics` | Launch Statistics is carrying metric Registers Per Thread.
- investigate `section` `Occupancy` @ `Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- investigate `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- investigate `rule` `SOLBottleneck` @ `None` | SOLBottleneck
- investigate `rule` `TheoreticalOccupancy` @ `None` | TheoreticalOccupancy

## Handoff to node_c

- target hotspot: `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` = `197.0` | Launch Statistics is carrying metric Registers Per Thread.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` = `16.6` | Occupancy is carrying metric Achieved Occupancy.
- target hotspot: `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` = `16.67` | Occupancy is carrying metric Theoretical Occupancy.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` = `20.88` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` = `28.77` | GPU Speed Of Light Throughput is carrying metric L2 Cache Throughput.
- target hotspot: `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `Memory Throughput` = `45.97` | GPU Speed Of Light Throughput is carrying metric Memory Throughput.
- guardrail: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `48.06` | Tensor activity is part of the active bottleneck picture and should not drop after the next code edit.
- guardrail: `sm__warps_active.avg.pct_of_peak_sustained_active` `non_decreasing` from `16.59` | Latency-hiding is already weak; active warps should not regress.
- guardrail: `smsp__warp_issue_stalled_barrier_per_warp_active.pct` `non_increasing` from `7.59` | barrier stalls are consuming 7.59% of active warp issue slots.
- guardrail: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` `non_increasing` from `4.54` | mio throttle stalls are consuming 4.54% of active warp issue slots.
- recheck `section` `Launch Statistics` @ `Launch Statistics` | `Registers Per Thread` | Launch Statistics is carrying metric Registers Per Thread.
- recheck `section` `Occupancy` @ `Occupancy` | `Achieved Occupancy` | Occupancy is carrying metric Achieved Occupancy.
- recheck `section` `Occupancy` @ `Occupancy` | `Theoretical Occupancy` | Occupancy is carrying metric Theoretical Occupancy.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | GPU Speed Of Light Throughput is carrying metric DRAM Throughput.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `DRAM Throughput` | Previous delta was improved in the improved bucket.
- recheck `section` `GPU Speed Of Light Throughput` @ `GPU Speed Of Light Throughput` | `L2 Cache Throughput` | Previous delta was regressed in the regressed bucket.
