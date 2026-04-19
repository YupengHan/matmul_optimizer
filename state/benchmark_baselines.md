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
- kernel tag: `bf16_gemm_v1_f5de2e9`
- runtime: `65.617920 ms`
- TFLOP/s: `11.079587 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_224421_bf16_gemm_v1_f5de2e9`
- summary json: `runs/20260418_224421_bf16_gemm_v1_f5de2e9/summary.json`
- measured commit: `f5de2e9ce546b72f0e2b1ecde0fbe5a766a31e42`

## Gap

- absolute runtime gap: `39.700031 ms`
- runtime ratio: `2.531762x` slower than CUTLASS
