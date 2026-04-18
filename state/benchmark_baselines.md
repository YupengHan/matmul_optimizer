# Benchmark baselines

## Official benchmark

- dataset: `fixed_bf16_gemm_v1`
- metric of record: median kernel runtime on `case_00_seed_3407`
- timing excludes file I/O
- correctness must pass before a performance result is accepted

## CUTLASS baseline

- status: NOT RUN
- runtime: N/A
- TFLOP/s: N/A
- date: N/A
- artifact run dir: N/A
- notes: CUTLASS reference runner has not been added or measured yet

## Best custom kernel

- status: HOST BASELINE RECORDED
- kernel tag: `bf16_gemm_v1_host_v0`
- runtime: `802.8425598 ms` median on `case_00_seed_3407`
- TFLOP/s: `0.9055566534`
- date: `2026-04-18`
- artifact run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- notes: correctness passed on all 3 configured cases under the current tolerance policy; Nsight Compute recorded both `ncu_profile.ncu-rep` and `ncu_metrics.csv`; quick read shows `sm__pipe_tensor_cycles_active = 0`, which matches the current placeholder shared-memory implementation

## Gap

- absolute runtime gap: UNKNOWN
- percent gap: UNKNOWN
- current view of limiting factor: a valid host-side custom-kernel baseline now exists, but there is still no CUTLASS reference result to compare against
