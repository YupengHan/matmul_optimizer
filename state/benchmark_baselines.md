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
- kernel tag: `bf16_gemm_v1_273d63c`
- runtime: `28.949504 ms`
- TFLOP/s: `25.113364 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_001122_bf16_gemm_v1_273d63c`
- summary json: `runs/20260420_001122_bf16_gemm_v1_273d63c/summary.json`
- measured commit: `273d63c0dca706eb94e279d165295463933a4b5c`

## Gap

- absolute runtime gap: `3.031615 ms`
- runtime ratio: `1.116970x` slower than CUTLASS
