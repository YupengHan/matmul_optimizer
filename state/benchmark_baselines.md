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
- kernel tag: `bf16_gemm_v1_da19f01`
- runtime: `46.771713 ms`
- TFLOP/s: `15.543998 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_234153_bf16_gemm_v1_da19f01`
- summary json: `runs/20260418_234153_bf16_gemm_v1_da19f01/summary.json`
- measured commit: `da19f01bfb3793b3cca3cc67fd521b0fe4fcf2b7`

## Gap

- absolute runtime gap: `20.853825 ms`
- runtime ratio: `1.804611x` slower than CUTLASS
