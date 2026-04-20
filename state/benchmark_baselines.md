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
- kernel tag: `bf16_gemm_v1_4e5579e`
- runtime: `24.570881 ms`
- TFLOP/s: `29.588659 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_084915_bf16_gemm_v1_4e5579e`
- summary json: `runs/20260420_084915_bf16_gemm_v1_4e5579e/summary.json`
- measured commit: `4e5579ec72e9b1f05820c895c0315235d66f30cd`

## Gap

- absolute runtime gap: `-1.347008 ms`
- runtime ratio: `0.948028x` slower than CUTLASS
