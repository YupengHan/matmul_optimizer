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
- kernel tag: `bf16_gemm_v1_85bb65b`
- runtime: `30.974368 ms`
- TFLOP/s: `23.471647 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_185736_bf16_gemm_v1_85bb65b`
- summary json: `runs/20260419_185736_bf16_gemm_v1_85bb65b/summary.json`
- measured commit: `85bb65b526d3810345e8a9d233a2679a9d41150e`

## Gap

- absolute runtime gap: `5.056479 ms`
- runtime ratio: `1.195096x` slower than CUTLASS
