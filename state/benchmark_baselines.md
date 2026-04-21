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
- kernel tag: `bf16_gemm_v1_489574e`
- runtime: `24.164272 ms`
- TFLOP/s: `30.086543 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_235922_bf16_gemm_v1_489574e`
- summary json: `runs/20260420_235922_bf16_gemm_v1_489574e/summary.json`
- measured commit: `489574ed5013268dbb79c634450d9a60155a294a`

## Gap

- absolute runtime gap: `-1.753616 ms`
- runtime ratio: `0.932340x` slower than CUTLASS
