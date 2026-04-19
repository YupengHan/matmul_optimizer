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
- kernel tag: `bf16_gemm_v1_af155a5`
- runtime: `145.344559 ms`
- TFLOP/s: `5.002041 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_201228_bf16_gemm_v1_af155a5`
- summary json: `runs/20260418_201228_bf16_gemm_v1_af155a5/summary.json`
- measured commit: `af155a5bdaa475a7edba5ed1957b25a46454536e`

## Gap

- absolute runtime gap: `119.426670 ms`
- runtime ratio: `5.607886x` slower than CUTLASS
