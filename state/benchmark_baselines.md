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
- kernel tag: `bf16_gemm_v1_1e399d8`
- runtime: `33.366047 ms`
- TFLOP/s: `21.789199 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_135930_bf16_gemm_v1_1e399d8`
- summary json: `runs/20260419_135930_bf16_gemm_v1_1e399d8/summary.json`
- measured commit: `1e399d80f7b02720493e3275ecb2c6865cbe1e63`

## Gap

- absolute runtime gap: `7.448158 ms`
- runtime ratio: `1.287375x` slower than CUTLASS
