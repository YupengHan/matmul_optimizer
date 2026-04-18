# Benchmark baselines

## Official benchmark

- dataset: `fixed_bf16_gemm_v1`
- metric of record: median kernel runtime on `case_00_seed_3407`
- timing excludes file I/O
- correctness must pass before a performance result is accepted

## CUTLASS baseline

- status: RECORDED
- kernel tag: `cutlass_ref_v0`
- runtime: `25.91788864 ms` median on `case_00_seed_3407`
- TFLOP/s: `28.05087373`
- correctness: PASS on all 3 configured cases under the current tolerance policy
- date: `2026-04-18`
- artifact run dir: `runs/20260418_115324_cutlass_ref_v0`
- notes: first CUTLASS baseline and first CUTLASS Nsight Compute artifacts now exist; `ncu_profile.ncu-rep` and `ncu_metrics.csv` were both recorded, with headline metrics including `sm__pipe_tensor_cycles_active = 49.25`, `sm__throughput = 49.39`, `dram__throughput = 42.76`, and `launch__occupancy_limit_registers = 2`

## Best custom kernel

- status: HOST BASELINE RECORDED
- kernel tag: `bf16_gemm_v1_host_v0`
- runtime: `802.8425598 ms` median on `case_00_seed_3407`
- TFLOP/s: `0.9055566534`
- date: `2026-04-18`
- artifact run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- notes: correctness passed on all 3 configured cases under the current tolerance policy; Nsight Compute recorded both `ncu_profile.ncu-rep` and `ncu_metrics.csv`; quick read shows `sm__pipe_tensor_cycles_active = 0`, which matches the current placeholder shared-memory implementation

## Gap

- absolute runtime gap: `776.92467116 ms` with `bf16_gemm_v1_host_v0` slower than CUTLASS on `case_00_seed_3407`
- percent gap: `2997.63874269%` slower than CUTLASS, or `30.97638743x` the CUTLASS runtime
- current view of limiting factor: the gap is still architectural rather than procedural; CUTLASS now shows a live Tensor Core path with `sm__pipe_tensor_cycles_active = 49.25`, while the current custom baseline still shows `sm__pipe_tensor_cycles_active = 0`
