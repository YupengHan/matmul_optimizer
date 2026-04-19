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
- kernel tag: `bf16_gemm_v1_c2f2bec`
- runtime: `34.234447 ms`
- TFLOP/s: `21.236488 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_132725_bf16_gemm_v1_c2f2bec`
- summary json: `runs/20260419_132725_bf16_gemm_v1_c2f2bec/summary.json`
- measured commit: `c2f2bec47c9cba44f35cf7d260893f0416a4d251`

## Gap

- absolute runtime gap: `8.316559 ms`
- runtime ratio: `1.320881x` slower than CUTLASS
