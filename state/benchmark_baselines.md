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
- kernel tag: `bf16_gemm_v1_d52137a`
- runtime: `26.093568 ms`
- TFLOP/s: `27.862017 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_010120_bf16_gemm_v1_d52137a`
- summary json: `runs/20260420_010120_bf16_gemm_v1_d52137a/summary.json`
- measured commit: `d52137aeec77eeeeffce6d3af05468487e1ea98c`

## Gap

- absolute runtime gap: `0.175679 ms`
- runtime ratio: `1.006778x` slower than CUTLASS
