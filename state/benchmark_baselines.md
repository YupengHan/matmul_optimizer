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
- kernel tag: `bf16_gemm_v1_57d08c3`
- runtime: `24.713584 ms`
- TFLOP/s: `29.417806 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_084312_bf16_gemm_v1_57d08c3`
- summary json: `runs/20260420_084312_bf16_gemm_v1_57d08c3/summary.json`
- measured commit: `57d08c3396876293a5e7c223a96cb3da09cca4a9`

## Gap

- absolute runtime gap: `-1.204305 ms`
- runtime ratio: `0.953534x` slower than CUTLASS
