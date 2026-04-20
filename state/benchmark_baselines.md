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
- kernel tag: `bf16_gemm_v1_0d78758`
- runtime: `29.325824 ms`
- TFLOP/s: `24.791100 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_222734_bf16_gemm_v1_0d78758`
- summary json: `runs/20260419_222734_bf16_gemm_v1_0d78758/summary.json`
- measured commit: `0d787589a75b35984fb169106135c77436806bc6`

## Gap

- absolute runtime gap: `3.407935 ms`
- runtime ratio: `1.131490x` slower than CUTLASS
