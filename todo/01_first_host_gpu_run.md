# Task 01: First Host GPU Run

## Goal

Run the existing custom runner on the host terminal that can access the GPU and produce the first valid run directory under `runs/`.

## Why this task exists

The Codex sandbox cannot see the GPU, but the host terminal can. The repo already contains:

- dataset generator
- `build/custom_runner`
- `scripts/eval_kernel.py`

So the next missing artifact is not new code. It is a real host-side run result.

## Read first

- `README.md`
- `configs/fixed_bf16_gemm_v1.json`
- `scripts/eval_kernel.py`
- `src/runner/main.cpp`
- `configs/ncu_metrics_core.txt`

## Do not do

- do not change the benchmark shape
- do not edit tolerance policy yet unless correctness clearly fails on the host
- do not start CUTLASS work in this task

## Commands to run on the host terminal

```bash
cd /home/aice/Desktop/matmul_optimizer

python scripts/generate_fixed_bf16_dataset.py

cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j

python scripts/eval_kernel.py \
  --runner build/custom_runner \
  --kernel-tag bf16_gemm_v1_host_v0 \
  --config configs/fixed_bf16_gemm_v1.json \
  --dataset-root artifacts/datasets \
  --runs-root runs \
  --ncu-bin ncu
```

## What success looks like

Find the latest run directory:

```bash
ls -td runs/* | head -n1
```

The new run directory should contain at least:

- `summary.json`
- `summary.md`
- `perf_case_00_seed_3407.json`
- `ncu_profile.ncu-rep`
- `ncu_metrics.csv`

## What to inspect immediately

```bash
RUN_DIR=$(ls -td runs/*_bf16_gemm_v1_host_v0 | head -n1)

echo "$RUN_DIR"
sed -n '1,200p' "$RUN_DIR/summary.md"
jq '.perf_run, .ncu' "$RUN_DIR/summary.json"
sed -n '1,120p' "$RUN_DIR/ncu_metrics.csv"
```

## Definition of done

- a new `runs/<timestamp>_bf16_gemm_v1_host_v0/` exists
- correctness results are recorded
- performance result is recorded
- `ncu_profile.ncu-rep` exists
- `ncu_metrics.csv` exists
- no code changes are required unless the host run exposes a real bug

## If the task fails

Record the exact failure mode:

- build failure
- correctness failure
- perf failure
- `ncu` not found
- `ncu` permission issue
- CUDA runtime failure on the host

Do not start fixing CUTLASS or optimization ideas in this task. Only unblock the first real host-side run.

## Suggested prompt for VSCode chat

```text
Please complete todo/01_first_host_gpu_run.md exactly as written. Do not change benchmark shape or start CUTLASS work. Your goal is to produce the first successful host-side run artifacts under runs/ and summarize whether correctness, perf, and NCU all succeeded.
```
