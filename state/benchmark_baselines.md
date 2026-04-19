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
- kernel tag: `bf16_gemm_v1_16a98f7`
- runtime: `37.285807 ms`
- TFLOP/s: `19.498557 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_015554_bf16_gemm_v1_16a98f7`
- summary json: `runs/20260419_015554_bf16_gemm_v1_16a98f7/summary.json`
- measured commit: `16a98f7af190c1b90503973135cbf4b754cdad0a`

## Gap

- absolute runtime gap: `11.367918 ms`
- runtime ratio: `1.438613x` slower than CUTLASS
