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
- kernel tag: `bf16_gemm_v1_df5bac2`
- runtime: `24.164352 ms`
- TFLOP/s: `30.086443 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_224147_bf16_gemm_v1_df5bac2`
- summary json: `runs/20260420_224147_bf16_gemm_v1_df5bac2/summary.json`
- measured commit: `df5bac281a2efef7f02478947a334a51b6510138`

## Gap

- absolute runtime gap: `-1.753536 ms`
- runtime ratio: `0.932343x` slower than CUTLASS
