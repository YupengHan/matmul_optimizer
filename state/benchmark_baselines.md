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
- kernel tag: `bf16_gemm_v1_8138da5`
- runtime: `97.885185 ms`
- TFLOP/s: `7.427267 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_212627_bf16_gemm_v1_8138da5`
- summary json: `runs/20260418_212627_bf16_gemm_v1_8138da5/summary.json`
- measured commit: `8138da55448e546af314940addc89fd3cadc56ff`

## Gap

- absolute runtime gap: `71.967297 ms`
- runtime ratio: `3.776742x` slower than CUTLASS
