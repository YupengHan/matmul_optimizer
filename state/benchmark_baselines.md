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
- kernel tag: `bf16_gemm_v1_1181247`
- runtime: `24.422464 ms`
- TFLOP/s: `29.768471 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_185423_bf16_gemm_v1_1181247`
- summary json: `runs/20260420_185423_bf16_gemm_v1_1181247/summary.json`
- measured commit: `1181247a12bfd0978dd155838558142b6386710e`

## Gap

- absolute runtime gap: `-1.495424 ms`
- runtime ratio: `0.942301x` slower than CUTLASS
