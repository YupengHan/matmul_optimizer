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
- kernel tag: `bf16_gemm_v1_79cdb43`
- runtime: `42.564560 ms`
- TFLOP/s: `17.080393 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_010405_bf16_gemm_v1_79cdb43`
- summary json: `runs/20260419_010405_bf16_gemm_v1_79cdb43/summary.json`
- measured commit: `79cdb4341e0f3a30327d811f49424bb324cbbf43`

## Gap

- absolute runtime gap: `16.646671 ms`
- runtime ratio: `1.642285x` slower than CUTLASS
