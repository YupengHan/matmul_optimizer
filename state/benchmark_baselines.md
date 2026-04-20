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
- kernel tag: `bf16_gemm_v1_11f0427`
- runtime: `29.116928 ms`
- TFLOP/s: `24.968960 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_000930_bf16_gemm_v1_11f0427`
- summary json: `runs/20260420_000930_bf16_gemm_v1_11f0427/summary.json`
- measured commit: `11f04271ca6d1544510b98163a61027d6cef8c5d`

## Gap

- absolute runtime gap: `3.199039 ms`
- runtime ratio: `1.123430x` slower than CUTLASS
