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
- kernel tag: `bf16_gemm_v1_1b9dbe3`
- runtime: `26.924031 ms`
- TFLOP/s: `27.002621 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_002759_bf16_gemm_v1_1b9dbe3`
- summary json: `runs/20260420_002759_bf16_gemm_v1_1b9dbe3/summary.json`
- measured commit: `1b9dbe3d306090b4f1762f1e1a504c13d2ab5d92`

## Gap

- absolute runtime gap: `1.006143 ms`
- runtime ratio: `1.038820x` slower than CUTLASS
