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
- kernel tag: `bf16_gemm_v1_22b4466`
- runtime: `25.677312 ms`
- TFLOP/s: `28.313689 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_073721_bf16_gemm_v1_22b4466`
- summary json: `runs/20260420_073721_bf16_gemm_v1_22b4466/summary.json`
- measured commit: `22b4466b0ff3ca82c4a03efa03d07462cb5ca69c`

## Gap

- absolute runtime gap: `-0.240577 ms`
- runtime ratio: `0.990718x` slower than CUTLASS
