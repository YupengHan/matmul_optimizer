# Latest Nsight Compute summary

- source run id: `20260418_111959_bf16_gemm_v1_host_v0`
- source run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- status: `available`
- kernel name: `matmul_optimizer::<unnamed>::bf16_gemm_v1_kernel(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *, int, int, int)`
- block size: `256`
- grid size: `196344`
- registers / thread: `36`
- shared mem / block allocated: `3072`
- raw csv path: `runs/20260418_111959_bf16_gemm_v1_host_v0/ncu_metrics.csv`
- raw rep path: `runs/20260418_111959_bf16_gemm_v1_host_v0/ncu_profile.ncu-rep`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `0`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `99.11`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `99.11`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `9.29`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `7.47`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `99.94`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `13.73`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `12.70`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `0.91`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `57.07`
- `launch__occupancy_limit_registers`: `6`
