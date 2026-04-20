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
- kernel tag: `bf16_gemm_v1_e26d834`
- runtime: `25.974272 ms`
- TFLOP/s: `27.989983 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_012953_bf16_gemm_v1_e26d834`
- summary json: `runs/20260420_012953_bf16_gemm_v1_e26d834/summary.json`
- measured commit: `e26d834e2583eaa041749b99e07234b9454d49e5`

## Gap

- absolute runtime gap: `0.056383 ms`
- runtime ratio: `1.002175x` slower than CUTLASS
