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
- kernel tag: `bf16_gemm_v1_68c21ac`
- runtime: `24.177664 ms`
- TFLOP/s: `30.069879 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_221009_bf16_gemm_v1_68c21ac`
- summary json: `runs/20260420_221009_bf16_gemm_v1_68c21ac/summary.json`
- measured commit: `68c21acd26439775c646252dbb0e52d247ea9f47`

## Gap

- absolute runtime gap: `-1.740225 ms`
- runtime ratio: `0.932856x` slower than CUTLASS
