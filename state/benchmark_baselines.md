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
- kernel tag: `bf16_gemm_v1_01d0040`
- runtime: `43.697664 ms`
- TFLOP/s: `16.637489 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_235548_bf16_gemm_v1_01d0040`
- summary json: `runs/20260418_235548_bf16_gemm_v1_01d0040/summary.json`
- measured commit: `01d00409efc03fdf555fef3ea7cc4efd403a720a`

## Gap

- absolute runtime gap: `17.779776 ms`
- runtime ratio: `1.686004x` slower than CUTLASS
