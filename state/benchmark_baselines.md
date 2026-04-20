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
- kernel tag: `bf16_gemm_v1_be44358`
- runtime: `29.204992 ms`
- TFLOP/s: `24.893669 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_235558_bf16_gemm_v1_be44358`
- summary json: `runs/20260419_235558_bf16_gemm_v1_be44358/summary.json`
- measured commit: `be44358062dd87db8692cf1a8ce8017bab55a65d`

## Gap

- absolute runtime gap: `3.287104 ms`
- runtime ratio: `1.126828x` slower than CUTLASS
