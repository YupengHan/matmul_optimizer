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
- kernel tag: `bf16_gemm_v1_eecbb72`
- runtime: `82.266624 ms`
- TFLOP/s: `8.837356 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_221951_bf16_gemm_v1_eecbb72`
- summary json: `runs/20260418_221951_bf16_gemm_v1_eecbb72/summary.json`
- measured commit: `eecbb72cf2ce923b80d7eab679b5355a3873fc88`

## Gap

- absolute runtime gap: `56.348736 ms`
- runtime ratio: `3.174125x` slower than CUTLASS
