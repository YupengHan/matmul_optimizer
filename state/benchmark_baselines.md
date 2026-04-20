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
- kernel tag: `bf16_gemm_v1_de7e8be`
- runtime: `24.849423 ms`
- TFLOP/s: `29.256994 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_083902_bf16_gemm_v1_de7e8be`
- summary json: `runs/20260420_083902_bf16_gemm_v1_de7e8be/summary.json`
- measured commit: `de7e8be6e77487fbeecd095db66faa31c991de1e`

## Gap

- absolute runtime gap: `-1.068465 ms`
- runtime ratio: `0.958775x` slower than CUTLASS
