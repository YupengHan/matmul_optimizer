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
- kernel tag: `bf16_gemm_v1_c26ac4f`
- runtime: `27.022336 ms`
- TFLOP/s: `26.904388 TFLOP/s`
- correctness: `PASS`
- run dir: `runs/20260420_002119_bf16_gemm_v1_c26ac4f`
- summary json: `runs/20260420_002119_bf16_gemm_v1_c26ac4f/summary.json`
- measured commit: `c26ac4fdc00ad89cefc324b30d4fc8758fb4d0af`

## Gap

- absolute runtime gap: `1.104447 ms`
- runtime ratio: `1.042613x` slower than CUTLASS
