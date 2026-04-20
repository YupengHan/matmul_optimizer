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
- kernel tag: `bf16_gemm_v1_f2b7c06`
- runtime: `24.895488 ms`
- TFLOP/s: `29.202859 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_082007_bf16_gemm_v1_f2b7c06`
- summary json: `runs/20260420_082007_bf16_gemm_v1_f2b7c06/summary.json`
- measured commit: `f2b7c066d6bb259ec12a6d7ccfe63f381a8e8f10`

## Gap

- absolute runtime gap: `-1.022401 ms`
- runtime ratio: `0.960552x` slower than CUTLASS
