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
- kernel tag: `bf16_gemm_v1_host_v0`
- runtime: `802.842560 ms`
- TFLOP/s: `0.905557 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- summary json: `runs/20260418_111959_bf16_gemm_v1_host_v0/summary.json`
- measured commit: `9e20de18aa67dc6b5eb289d5e8e4c203dae37fa6`

## Gap

- absolute runtime gap: `776.924671 ms`
- runtime ratio: `30.976387x` slower than CUTLASS
