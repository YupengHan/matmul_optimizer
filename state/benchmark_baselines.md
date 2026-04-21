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
- kernel tag: `bf16_gemm_v1_0893f2c`
- runtime: `24.419329 ms`
- TFLOP/s: `29.772294 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_220130_bf16_gemm_v1_0893f2c`
- summary json: `runs/20260420_220130_bf16_gemm_v1_0893f2c/summary.json`
- measured commit: `0893f2c709f4c3d8d592b75fb4df066f13a5bafa`

## Gap

- absolute runtime gap: `-1.498560 ms`
- runtime ratio: `0.942180x` slower than CUTLASS
