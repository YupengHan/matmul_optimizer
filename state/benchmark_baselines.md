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
- kernel tag: `bf16_gemm_v1_8a2834a`
- runtime: `27.227264 ms`
- TFLOP/s: `26.701890 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_001707_bf16_gemm_v1_8a2834a`
- summary json: `runs/20260420_001707_bf16_gemm_v1_8a2834a/summary.json`
- measured commit: `8a2834ad9966fb75ef7c310ad5850de8c925ec5e`

## Gap

- absolute runtime gap: `1.309376 ms`
- runtime ratio: `1.050520x` slower than CUTLASS
