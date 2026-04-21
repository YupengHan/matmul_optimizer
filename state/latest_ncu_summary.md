# Latest Nsight Compute summary

- source run id: `20260421_110929_bf16_gemm_v1_342b1c5`
- source run dir: `runs/20260421_110929_bf16_gemm_v1_342b1c5`
- status: `available`
- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(256, 1, 1)`
- grid size: `(60, 25, 1)`
- registers / thread: `167.0`
- shared mem / block allocated: `42496.0`
- raw csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_metrics.csv`
- raw rep path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_profile.ncu-rep`
- raw detailed csv path: `runs/20260421_110929_bf16_gemm_v1_342b1c5/ncu_details.csv`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `36.77`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `36.28`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `32.96`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `15.87`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `18.19`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.66`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `8.32`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `2.19`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `6.77`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `0.84`
- `launch__occupancy_limit_registers`: `1.0`
