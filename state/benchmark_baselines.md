# Benchmark baselines

## Official benchmark

- dataset: `fixed_bf16_gemm_v1`
- metric of record: `median_runtime_ms`
- correctness must pass before a performance result is accepted

## CUTLASS baseline

- status: RECORDED
- kernel tag: `cutlass_ref_v0`
- runtime: `25.917889 ms`
- TFLOP/s: `28.050874 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_115324_cutlass_ref_v0`
- summary json: `runs/20260418_115324_cutlass_ref_v0/summary.json`

## Best custom kernel

- status: RECORDED
- kernel tag: `bf16_gemm_v1_b13027c`
- runtime: `30.052768 ms`
- TFLOP/s: `24.191430 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_191708_bf16_gemm_v1_b13027c`
- summary json: `runs/20260419_191708_bf16_gemm_v1_b13027c/summary.json`
- measured commit: `b13027cdde2a90d1f00f3bd9b1e6b355ea15f2d9`

## Gap

- absolute runtime gap: `4.134879 ms`
- runtime ratio: `1.159538x` slower than CUTLASS
