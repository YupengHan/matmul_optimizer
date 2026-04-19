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
- kernel tag: `bf16_gemm_v1_ea27d5a`
- runtime: `38.473728 ms`
- TFLOP/s: `18.896516 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_013130_bf16_gemm_v1_ea27d5a`
- summary json: `runs/20260419_013130_bf16_gemm_v1_ea27d5a/summary.json`
- measured commit: `ea27d5a906ceb46b0a4ec429d6d53f4a457620d6`

## Gap

- absolute runtime gap: `12.555840 ms`
- runtime ratio: `1.484447x` slower than CUTLASS
