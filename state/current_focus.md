# Current focus

- branch: `master`
- phase: `agent_input_package_ready`
- active execution node: hand the diagnosis agent `todo/agent_input_snapshot.md` plus `todo/agent_input_manifest.json` and keep the implementation node idle until exactly three directions are proposed
- current bottleneck belief: the custom placeholder kernel is still missing the Tensor Core execution path that CUTLASS is clearly using; the custom baseline showed `sm__pipe_tensor_cycles_active = 0`, `smsp__warp_issue_stalled_mio_throttle = 57.07`, and only `9.29%` DRAM throughput, while the accepted CUTLASS baseline shows `sm__pipe_tensor_cycles_active = 49.25`
- latest accepted custom run: `runs/20260418_111959_bf16_gemm_v1_host_v0` with correctness PASS on all 3 configured cases and `802.8425598 ms` median runtime on `case_00_seed_3407`
- latest accepted CUTLASS run: `runs/20260418_115324_cutlass_ref_v0` with correctness PASS on all 3 configured cases and `25.91788864 ms` median runtime on `case_00_seed_3407`
- current runtime gap to beat: `776.92467116 ms`, with the custom kernel currently `30.97638743x` slower than CUTLASS on the metric-of-record case
- prepared diagnosis handoff:
  - `todo/agent_input_snapshot.md`
  - `todo/agent_input_manifest.json`
- prior sandbox note: `runs/20260418_021152_bf16_gemm_v1` failed at `cudaMalloc` because the sandbox could not see the GPU
- immediate next action: run a diagnosis pass on the prepared handoff package and ask for exactly three optimization directions before changing the kernel again
