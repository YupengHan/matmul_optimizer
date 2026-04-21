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

## cuBLAS baseline

- status: RECORDED
- kernel tag: `cublas_ref_clean_post_cleanup`
- runtime: `22.000000 ms`
- TFLOP/s: `33.046337 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260421_150524_cublas_ref_clean_post_cleanup`
- summary json: `runs/20260421_150524_cublas_ref_clean_post_cleanup/summary.json`
- ncu summary json: `runs/20260421_150524_cublas_ref_clean_post_cleanup/ncu_summary.json`
- ncu analysis json: `runs/20260421_150524_cublas_ref_clean_post_cleanup/ncu_analysis.json`
- ncu analysis md: `runs/20260421_150524_cublas_ref_clean_post_cleanup/ncu_analysis.md`
- ncu rep path: `runs/20260421_150524_cublas_ref_clean_post_cleanup/ncu_profile.ncu-rep`

## Best custom kernel

- status: RECORDED
- kernel tag: `bf16_gemm_v1_489574e`
- runtime: `24.164272 ms`
- TFLOP/s: `30.086543 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_235922_bf16_gemm_v1_489574e`
- summary json: `runs/20260420_235922_bf16_gemm_v1_489574e/summary.json`
- ncu summary json: `state/latest_ncu_summary.json`
- measured commit: `489574ed5013268dbb79c634450d9a60155a294a`

## Gap

- absolute runtime gap vs CUTLASS: `-1.753616 ms`
- runtime ratio vs CUTLASS: `0.932340x` of CUTLASS runtime (faster)
- absolute runtime gap vs cuBLAS: `2.164272 ms`
- runtime ratio vs cuBLAS: `1.098376x` of cuBLAS runtime (slower)
