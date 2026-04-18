# Current focus

- branch: `master`
- phase: `post_cutlass_baseline_gap_analysis`
- active execution node: compare `runs/20260418_115324_cutlass_ref_v0` against `runs/20260418_111959_bf16_gemm_v1_host_v0` and use the NCU delta to choose the first real kernel rewrite
- current bottleneck belief: the custom placeholder kernel is still missing the Tensor Core execution path that CUTLASS is clearly using; the custom baseline showed `sm__pipe_tensor_cycles_active = 0`, while the accepted CUTLASS baseline shows `sm__pipe_tensor_cycles_active = 49.25`
- latest accepted host run: `runs/20260418_115324_cutlass_ref_v0` with correctness PASS on all 3 configured cases and `25.91788864 ms` median runtime on `case_00_seed_3407`
- latest accepted custom run: `runs/20260418_111959_bf16_gemm_v1_host_v0` with correctness PASS on all 3 configured cases and `802.8425598 ms` median runtime on `case_00_seed_3407`
- current runtime gap to beat: `776.92467116 ms`, with the custom kernel currently `30.97638743x` slower than CUTLASS on the metric-of-record case
- prior sandbox note: `runs/20260418_021152_bf16_gemm_v1` failed at `cudaMalloc` because the sandbox could not see the GPU
- immediate next action: design and implement the first Tensor Core-aware custom kernel revision, then re-run the same harness and NCU capture against the CUTLASS baseline
