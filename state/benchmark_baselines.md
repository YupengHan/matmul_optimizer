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
- kernel tag: `bf16_gemm_v1_3d01edf`
- runtime: `30.062544 ms`
- TFLOP/s: `24.183563 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_190546_bf16_gemm_v1_3d01edf`
- summary json: `runs/20260419_190546_bf16_gemm_v1_3d01edf/summary.json`
- measured commit: `3d01edf5053f250aa4096cda3efec53e1e8b894b`

## Gap

- absolute runtime gap: `4.144655 ms`
- runtime ratio: `1.159915x` slower than CUTLASS
