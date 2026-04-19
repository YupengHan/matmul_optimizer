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
- kernel tag: `bf16_gemm_v1_33e1461`
- runtime: `41.534977 ms`
- TFLOP/s: `17.503788 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_011243_bf16_gemm_v1_33e1461`
- summary json: `runs/20260419_011243_bf16_gemm_v1_33e1461/summary.json`
- measured commit: `33e1461e09c0f90b0896452a94c16277f2a251db`

## Gap

- absolute runtime gap: `15.617088 ms`
- runtime ratio: `1.602560x` slower than CUTLASS
