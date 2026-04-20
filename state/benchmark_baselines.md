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
- kernel tag: `bf16_gemm_v1_17a33b2`
- runtime: `25.529328 ms`
- TFLOP/s: `28.477812 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_074331_bf16_gemm_v1_17a33b2`
- summary json: `runs/20260420_074331_bf16_gemm_v1_17a33b2/summary.json`
- measured commit: `17a33b29fc2405c9fb3c5602d09a1c52bc42b32d`

## Gap

- absolute runtime gap: `-0.388560 ms`
- runtime ratio: `0.985008x` slower than CUTLASS
