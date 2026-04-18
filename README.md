# matmul_optimizer

Shape-specialized, AI-assisted CUDA kernel optimization for a fixed BF16 GEMM on a single RTX 3070 Laptop GPU.

## Goal

This repository is designed to demonstrate a practical workflow for:

1. fixing one challenging BF16 GEMM shape,
2. benchmarking a custom CUDA kernel against a stable local dataset,
3. profiling with Nsight Compute,
4. using AI + heuristics + human review to iterate on kernel changes,
5. and trying to beat a CUTLASS baseline on **one fixed workload**.

The repo is intentionally **script-first** for execution-critical steps. LLM/agent tokens are reserved for diagnosis, idea generation, and out-of-box exploration.

## Benchmark target

Current fixed workload (`fixed_bf16_gemm_v1`):

- `A[m, k] * B[k, n] = C[m, n]`
- `m = 6464`
- `n = 7776`
- `k = 7232`
- all dimensions are multiples of 32
- all three dimensions are **not** multiples of 128
- dtype: BF16 inputs, FP32 reference accumulation, BF16 output reference also stored

Why this shape:

- big enough to produce stable kernel timings on a single mobile 3070-class GPU,
- still safely inside typical 8 GB VRAM constraints,
- large enough to make Tensor Core scheduling and memory movement matter,
- slightly irregular versus common CTA tile shapes, which leaves room for shape-specialized optimization.

## Repository layout

```text
matmul_optimizer/
├── README.md
├── .gitignore
├── .gitmessage
├── configs/
│   ├── fixed_bf16_gemm_v1.json
│   └── ncu_metrics_core.txt
├── docs/
│   ├── benchmark_spec.md
│   ├── pipeline_graph.md
│   ├── heuristics.md
│   └── commit_convention.md
├── include/
│   ├── kernel_api.h
│   └── runner_contract.h
├── scripts/
│   ├── generate_fixed_bf16_dataset.py
│   ├── eval_kernel.py
│   └── run_cutlass_baseline.py
├── src/
│   ├── kernels/
│   │   └── bf16_gemm_v1.cu
│   └── runner/
│       └── main.cpp
├── state/
│   ├── README.md
│   ├── progress.md
│   ├── current_focus.md
│   ├── human_review.md
│   └── benchmark_baselines.md
├── artifacts/
│   └── README.md
└── runs/
```

## Current repository status

As of `2026-04-18`, the repository is past the pure scaffold stage.

What is already in place:

- deterministic dataset generation via `scripts/generate_fixed_bf16_dataset.py`
- a compilable CUDA runner target: `build/custom_runner`
- a callable placeholder kernel in `src/kernels/bf16_gemm_v1.cu`
- an evaluation orchestrator in `scripts/eval_kernel.py`
- local state tracking under `state/`

What has been verified in this workspace:

- `cmake -S . -B build` succeeds
- `cmake --build build -j 4` succeeds
- the fixed dataset manifest and generation summary exist locally under `artifacts/datasets/fixed_bf16_gemm_v1/`
- an end-to-end evaluation attempt exists at `runs/20260418_021152_bf16_gemm_v1/`

Current measurement status:

- the checked-in run under `runs/20260418_021152_bf16_gemm_v1/` was launched from the Codex sandbox and failed at `cudaMalloc` with `no CUDA-capable device is detected`
- that failure reflects the sandbox runtime environment, not a confirmed project-level GPU bring-up failure on the host machine
- per the current operator note, the host terminal outside Codex can access the GPU
- the repo still does **not** yet contain a valid committed custom-kernel runtime or CUTLASS baseline

## Source layout rules

- `src/runner/main.cpp` is the stable runner entrypoint that future CMake targets should compile into `custom_runner`.
- Versioned CUDA kernels live under `src/kernels/` and should follow `bf16_gemm_vN.cu`.
- Public runner and kernel boundaries belong in `include/`; avoid putting shared contracts inside versioned `.cu` files.
- `src/common/` is intentionally not created yet. The current shared surface is small enough that a second internal subtree would only add churn.

## Workflow summary

### 1. Create the fixed dataset once

```bash
python scripts/generate_fixed_bf16_dataset.py
```

This generates a deterministic local dataset under `artifacts/datasets/fixed_bf16_gemm_v1/`.

### 2. Evaluate a kernel candidate

`eval_kernel.py` is the execution node that replaces the original `agent_a` idea.

Responsibilities:

- warm up the GPU,
- run correctness checks,
- run performance timing,
- launch Nsight Compute,
- write both raw artifacts (`.rep`, raw logs, CSV) and agent-readable summaries (`summary.json`, `summary.md`).

### 3. Diagnose the bottleneck

An agent reads:

- the latest evaluation summary,
- the NCU summary,
- `docs/heuristics.md`,
- the current progress state,
- and relevant git history.

It outputs **exactly three** optimization directions.

### 4. Implement one direction at a time

A second agent (or Codex CLI loop) applies one direction, compiles, runs the evaluation script, and prepares a candidate change for human review.

### 5. Compare against CUTLASS

`run_cutlass_baseline.py` is the script-oriented version of `agent_c`.  
Run it periodically and especially after long plateaus.

### 6. Do branch-only out-of-box exploration

This is `agent_d` territory:

- read git history,
- read old profiling artifacts,
- compare with CUTLASS behavior,
- try bolder hypotheses on a feature branch,
- merge only if correctness and performance both improve.

## Notes

- Generated datasets, run artifacts, NCU `.rep` files, and large binaries should **not** be committed to git.
- Git is used as long-term memory for:
  - performance-improving commits,
  - experiment rationale,
  - branch history,
  - and human review decisions.
- Public-facing narrative should always emphasize that this is a **shape-specialized optimization problem**, not a claim to beat CUTLASS on every GEMM.

## Immediate next steps

1. rerun the existing pipeline on a host where the RTX 3070 Laptop GPU is visible to CUDA,
2. capture the first valid correctness and performance result for `bf16_gemm_v1` from the host terminal and write the run artifacts back under `runs/`,
3. add a CUTLASS reference runner and record the first baseline in `state/benchmark_baselines.md`,
4. use Nsight Compute on the first successful host-side run to identify the highest-value optimization target,
5. start replacing the placeholder GEMM kernel with a Tensor Core-aware implementation.
