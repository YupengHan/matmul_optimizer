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
- kernel tag: `bf16_gemm_v1_3265675`
- runtime: `63.126495 ms`
- TFLOP/s: `11.516867 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_225011_bf16_gemm_v1_3265675`
- summary json: `runs/20260418_225011_bf16_gemm_v1_3265675/summary.json`
- measured commit: `3265675318dd0108296bfc9c83879cc130bb6351`

## Gap

- absolute runtime gap: `37.208607 ms`
- runtime ratio: `2.435634x` slower than CUTLASS
