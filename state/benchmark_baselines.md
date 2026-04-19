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
- kernel tag: `bf16_gemm_v1_aee3c09`
- runtime: `101.374962 ms`
- TFLOP/s: `7.171588 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_210900_bf16_gemm_v1_aee3c09`
- summary json: `runs/20260418_210900_bf16_gemm_v1_aee3c09/summary.json`
- measured commit: `aee3c09b51fbf78ad79f4ce5f68841449bab54a1`

## Gap

- absolute runtime gap: `75.457073 ms`
- runtime ratio: `3.911390x` slower than CUTLASS
