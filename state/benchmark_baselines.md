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
- kernel tag: `bf16_gemm_v1_91e446e`
- runtime: `54.136911 ms`
- TFLOP/s: `13.429274 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_225901_bf16_gemm_v1_91e446e`
- summary json: `runs/20260418_225901_bf16_gemm_v1_91e446e/summary.json`
- measured commit: `91e446eea2cf2de912e81e21c45653dcd227d591`

## Gap

- absolute runtime gap: `28.219023 ms`
- runtime ratio: `2.088786x` slower than CUTLASS
