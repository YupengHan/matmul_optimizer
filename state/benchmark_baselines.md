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
- kernel tag: `bf16_gemm_v1_5ae2249`
- runtime: `27.691520 ms`
- TFLOP/s: `26.254226 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_001545_bf16_gemm_v1_5ae2249`
- summary json: `runs/20260420_001545_bf16_gemm_v1_5ae2249/summary.json`
- measured commit: `5ae2249d5b7a8c9f9686021e82e20d1a24aa3bde`

## Gap

- absolute runtime gap: `1.773631 ms`
- runtime ratio: `1.068433x` slower than CUTLASS
