# Progress

## Objective

Beat the local CUTLASS baseline on a **single fixed BF16 GEMM shape** on an RTX 3070 Laptop GPU.

## Fixed workload

- dataset: `fixed_bf16_gemm_v1`
- shape: `m=6464, n=7776, k=7232`
- benchmark case: `case_00_seed_3407`
- correctness cases:
  - `case_00_seed_3407`
  - `case_01_seed_9713`
  - `case_02_seed_1729`

## Current status

- dataset generation scaffold: READY
- local dataset generation: READY
- evaluation harness scaffold: READY
- custom CUDA runner: READY
- placeholder custom kernel: READY
- first end-to-end evaluation attempt: COMPLETE
- CUTLASS baseline: TODO
- current best custom kernel: NO VALID GPU RESULT YET
- gap to CUTLASS: UNKNOWN

## Verified snapshot

- configured and built successfully with `cmake -S . -B build` and `cmake --build build -j 4`
- local dataset summary exists under `artifacts/datasets/fixed_bf16_gemm_v1/generation_summary.json`
- total generated dataset size is `1452.1171875 MiB` across 3 cases
- latest local evaluation attempt is `runs/20260418_021152_bf16_gemm_v1`
- that run failed before measurement because the current environment reported `cudaMalloc: no CUDA-capable device is detected`

## Iteration log

### Iteration 0 - repository scaffold

- established one fixed benchmark shape
- decided to keep the execution path script-first
- split the former `agent_b` into:
  - diagnosis node
  - implementation loop node
- reserved branch-heavy exploration for `agent_d`

### Iteration 1 - dataset + runner bring-up

- implemented deterministic dataset generation and wrote local manifests/checksums
- implemented `custom_runner` with:
  - dataset loading
  - correctness checking against `C_ref_fp32` and `C_ref_bf16`
  - timed perf loop with cache flush and percentile summary
- wired `scripts/eval_kernel.py` to the runner contract and run artifact layout
- compiled the CUDA target successfully
- executed the first end-to-end run locally
- observed an environment blocker instead of a kernel-level result:
  - `cudaMalloc: no CUDA-capable device is detected`

## Near-term next actions

1. rerun `build/custom_runner` on a CUDA-visible machine and capture the first accepted custom-kernel baseline
2. add and measure a CUTLASS reference runner on the same host
3. record both baselines in `state/benchmark_baselines.md`
4. profile the first successful run with Nsight Compute and choose the first optimization direction
