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
- kernel tag: `bf16_gemm_v1_5ab5302`
- runtime: `36.517889 ms`
- TFLOP/s: `19.908583 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_101256_bf16_gemm_v1_5ab5302`
- summary json: `runs/20260419_101256_bf16_gemm_v1_5ab5302/summary.json`
- measured commit: `5ab5302bd23e8cd1ff2fcd97dbfd5a35b1701ca9`

## Gap

- absolute runtime gap: `10.600000 ms`
- runtime ratio: `1.408984x` slower than CUTLASS
