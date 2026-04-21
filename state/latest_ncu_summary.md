# Latest Nsight Compute summary

- source run id: `20260421_111322_bf16_gemm_v1_f768e80`
- source run dir: `runs/20260421_111322_bf16_gemm_v1_f768e80`
- status: `available`
- kernel name: `void matmul_optimizer::<unnamed>::bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>(const __nv_bfloat16 *, const __nv_bfloat16 *, __nv_bfloat16 *)`
- block size: `(128, 1, 1)`
- grid size: `(60, 50, 1)`
- registers / thread: `200.0`
- shared mem / block allocated: `22016.0`
- raw csv path: `runs/20260421_111322_bf16_gemm_v1_f768e80/ncu_metrics.csv`
- raw rep path: `runs/20260421_111322_bf16_gemm_v1_f768e80/ncu_profile.ncu-rep`
- raw detailed csv path: `runs/20260421_111322_bf16_gemm_v1_f768e80/ncu_details.csv`

## Headline metrics

- `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: `48.41`
- `sm__throughput.avg.pct_of_peak_sustained_elapsed`: `47.84`
- `gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed`: `46.13`
- `dram__throughput.avg.pct_of_peak_sustained_elapsed`: `12.48`
- `lts__throughput.avg.pct_of_peak_sustained_elapsed`: `30.06`
- `sm__warps_active.avg.pct_of_peak_sustained_active`: `16.63`
- `smsp__warp_issue_stalled_barrier_per_warp_active.pct`: `5.47`
- `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: `7.16`
- `smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`: `2.16`
- `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: `3.64`
- `launch__occupancy_limit_registers`: `2.0`
