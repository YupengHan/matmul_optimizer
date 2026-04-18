# Benchmark baselines

## Official benchmark

- dataset: `fixed_bf16_gemm_v1`
- metric of record: median kernel runtime on `case_00_seed_3407`
- timing excludes file I/O
- correctness must pass before a performance result is accepted

## CUTLASS baseline

- status: NOT RUN
- runtime: N/A
- TFLOP/s: N/A
- date: N/A
- artifact run dir: N/A
- notes: CUTLASS reference runner has not been added or measured yet

## Best custom kernel

- status: BRING-UP ATTEMPT ONLY
- kernel tag: `bf16_gemm_v1`
- runtime: N/A
- TFLOP/s: N/A
- date: `2026-04-18`
- artifact run dir: `runs/20260418_021152_bf16_gemm_v1`
- notes: the first end-to-end run executed through `build/custom_runner`, but every run failed with `cudaMalloc: no CUDA-capable device is detected`, so there is still no accepted custom-kernel baseline

## Gap

- absolute runtime gap: UNKNOWN
- percent gap: UNKNOWN
- current view of limiting factor: blocked by environment bring-up; no valid GPU measurement yet
