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
- kernel tag: `bf16_gemm_v1_2872f92`
- runtime: `35.677088 ms`
- TFLOP/s: `20.377768 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_102608_bf16_gemm_v1_2872f92`
- summary json: `runs/20260419_102608_bf16_gemm_v1_2872f92/summary.json`
- measured commit: `2872f92585773d6f6a38c911cb76d010d4209366`

## Gap

- absolute runtime gap: `9.759199 ms`
- runtime ratio: `1.376543x` slower than CUTLASS
