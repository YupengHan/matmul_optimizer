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
- kernel tag: `bf16_gemm_v1_95056ed`
- runtime: `66.354687 ms`
- TFLOP/s: `10.956565 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_222639_bf16_gemm_v1_95056ed`
- summary json: `runs/20260418_222639_bf16_gemm_v1_95056ed/summary.json`
- measured commit: `95056ed21eab5afe9e0a7fc2faefa6e3b29e3903`

## Gap

- absolute runtime gap: `40.436798 ms`
- runtime ratio: `2.560189x` slower than CUTLASS
