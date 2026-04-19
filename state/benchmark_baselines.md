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
- kernel tag: `bf16_gemm_v1_4473555`
- runtime: `88.543102 ms`
- TFLOP/s: `8.210910 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_213511_bf16_gemm_v1_4473555`
- summary json: `runs/20260418_213511_bf16_gemm_v1_4473555/summary.json`
- measured commit: `2b09dbc797bd4f015003dd457b8692fbf6a7103d`

## Gap

- absolute runtime gap: `62.625214 ms`
- runtime ratio: `3.416293x` slower than CUTLASS
