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
- kernel tag: `bf16_gemm_v1_8346b48`
- runtime: `34.655231 ms`
- TFLOP/s: `20.978634 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_104631_bf16_gemm_v1_8346b48`
- summary json: `runs/20260419_104631_bf16_gemm_v1_8346b48/summary.json`
- measured commit: `8346b48ca5272beb86282fa09eb346dc73ab9f68`

## Gap

- absolute runtime gap: `8.737343 ms`
- runtime ratio: `1.337116x` slower than CUTLASS
