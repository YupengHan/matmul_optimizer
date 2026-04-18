# Task 03: Run CUTLASS Baseline and Capture NCU

## Goal

Use the new `cutlass_runner` to generate the first CUTLASS baseline run, including the first CUTLASS `ncu_profile.ncu-rep` and `ncu_metrics.csv`.

## Read first

- `scripts/run_cutlass_baseline.py`
- `scripts/eval_kernel.py`
- `configs/fixed_bf16_gemm_v1.json`
- `configs/ncu_metrics_core.txt`
- `state/benchmark_baselines.md`

## Preconditions

Before starting this task, all of the following must be true:

- `todo/01_first_host_gpu_run.md` is complete
- `todo/02_cutlass_runner.md` is complete
- `build/cutlass_runner` exists
- the host terminal can access the GPU
- `ncu` is installed and callable on the host

## Command to run on the host terminal

```bash
cd /home/aice/Desktop/matmul_optimizer

python scripts/run_cutlass_baseline.py \
  --runner build/cutlass_runner \
  --kernel-tag cutlass_ref_v0 \
  --config configs/fixed_bf16_gemm_v1.json \
  --dataset-root artifacts/datasets \
  --runs-root runs \
  --ncu-bin ncu
```

## What files must exist after success

Find the latest CUTLASS run:

```bash
CUTLASS_RUN=$(ls -td runs/*_cutlass_ref_v0 | head -n1)
echo "$CUTLASS_RUN"
```

This directory must contain:

- `summary.json`
- `summary.md`
- `perf_case_00_seed_3407.json`
- `ncu_profile.ncu-rep`
- `ncu_metrics.csv`

## Immediate inspection commands

```bash
sed -n '1,200p' "$CUTLASS_RUN/summary.md"
jq '.perf_run, .ncu' "$CUTLASS_RUN/summary.json"
sed -n '1,120p' "$CUTLASS_RUN/ncu_metrics.csv"
```

## Update state after success

Update:

- `state/benchmark_baselines.md`
- `state/progress.md`
- `state/current_focus.md`

Record:

- run directory
- median runtime
- TFLOP/s
- correctness status
- date
- that the first CUTLASS NCU report now exists

## Definition of done

- a CUTLASS baseline run exists under `runs/`
- `summary.json` reports valid perf data
- `ncu_profile.ncu-rep` exists for CUTLASS
- `ncu_metrics.csv` exists for CUTLASS
- state files point to the new baseline

## Suggested prompt for VSCode chat

```text
Please complete todo/03_cutlass_baseline_and_ncu.md. Assume build/cutlass_runner already exists. Your goal is to produce the first CUTLASS baseline run with summary.json, summary.md, ncu_profile.ncu-rep, and ncu_metrics.csv, then update the state files to record that baseline.
```
