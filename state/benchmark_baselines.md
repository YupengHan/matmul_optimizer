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
- kernel tag: `bf16_gemm_v1_c9d030a`
- runtime: `32.001088 ms`
- TFLOP/s: `22.718584 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260419_140646_bf16_gemm_v1_c9d030a`
- summary json: `runs/20260419_140646_bf16_gemm_v1_c9d030a/summary.json`
- measured commit: `c9d030a5022af8ce61bdcdb9b13e7ea85315ef52`

## Gap

- absolute runtime gap: `6.083199 ms`
- runtime ratio: `1.234710x` slower than CUTLASS
