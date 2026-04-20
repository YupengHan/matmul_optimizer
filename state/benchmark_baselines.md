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
- kernel tag: `bf16_gemm_v1_5dd9f0d`
- runtime: `29.432832 ms`
- TFLOP/s: `24.700968 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_221014_bf16_gemm_v1_5dd9f0d`
- summary json: `runs/20260419_221014_bf16_gemm_v1_5dd9f0d/summary.json`
- measured commit: `5dd9f0d02883a3b1debb9d3933a489c44bc0330d`

## Gap

- absolute runtime gap: `3.514943 ms`
- runtime ratio: `1.135618x` slower than CUTLASS
