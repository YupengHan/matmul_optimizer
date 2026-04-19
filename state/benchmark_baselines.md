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
- kernel tag: `bf16_gemm_v1_a4966f5`
- runtime: `298.095123 ms`
- TFLOP/s: `2.438884 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_195405_bf16_gemm_v1_a4966f5`
- summary json: `runs/20260418_195405_bf16_gemm_v1_a4966f5/summary.json`
- measured commit: `a4966f51626c0ae4e2d99e4e49fe26264639b123`

## Gap

- absolute runtime gap: `272.177235 ms`
- runtime ratio: `11.501520x` slower than CUTLASS
