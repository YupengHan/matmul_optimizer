# Current focus

- branch: `master`
- phase: `cutlass_baseline_pending`
- active execution node: `run_cutlass_baseline.py` after the accepted `custom_runner` host run
- current bottleneck belief: the placeholder shared-memory kernel is stable but far from optimized; the first host NCU run shows `sm__pipe_tensor_cycles_active = 0` and `smsp__warp_issue_stalled_mio_throttle_per_warp_active = 57.07`, which is consistent with not using a Tensor Core path yet
- latest accepted host run: `runs/20260418_111959_bf16_gemm_v1_host_v0` with correctness PASS on all 3 configured cases and `802.8425598 ms` median runtime on `case_00_seed_3407`
- prior sandbox note: `runs/20260418_021152_bf16_gemm_v1` failed at `cudaMalloc` because the sandbox could not see the GPU
- immediate next action: add and measure the CUTLASS baseline on the same host with the same artifact layout, then compare it against `bf16_gemm_v1_host_v0`
