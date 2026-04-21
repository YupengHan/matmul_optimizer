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
- kernel tag: `bf16_gemm_v1_2e4dd24`
- runtime: `24.444416 ms`
- TFLOP/s: `29.741738 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_180146_bf16_gemm_v1_2e4dd24`
- summary json: `runs/20260420_180146_bf16_gemm_v1_2e4dd24/summary.json`
- measured commit: `2e4dd246f55b505bd095c42b62c56dc497c8fde1`

## Gap

- absolute runtime gap: `-1.473473 ms`
- runtime ratio: `0.943148x` slower than CUTLASS
