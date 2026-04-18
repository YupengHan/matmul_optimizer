# Task 04: Prepare the Agent Input Package

## Goal

Package the minimal set of files that another agent should read to diagnose bottlenecks and propose the next optimization direction.

## Why this task exists

Agents do better with compact, structured inputs than with a raw `.ncu-rep` file alone.

The primary machine-readable inputs should be:

- `summary.json`
- `ncu_metrics.csv`
- `perf_case_00_seed_3407.json`

The `.ncu-rep` file should still be preserved for human inspection in `ncu-ui`.

## Read first

- `docs/heuristics.md`
- `state/progress.md`
- `state/benchmark_baselines.md`
- the latest custom-kernel run directory
- the latest CUTLASS run directory

## Build the package

Pick:

- the latest successful custom run
- the latest successful CUTLASS baseline run

Collect these files:

- `runs/<custom_run>/summary.json`
- `runs/<custom_run>/summary.md`
- `runs/<custom_run>/perf_case_00_seed_3407.json`
- `runs/<custom_run>/ncu_metrics.csv`
- `runs/<cutlass_run>/summary.json`
- `runs/<cutlass_run>/summary.md`
- `runs/<cutlass_run>/perf_case_00_seed_3407.json`
- `runs/<cutlass_run>/ncu_metrics.csv`

Optional for human review:

- `runs/<custom_run>/ncu_profile.ncu-rep`
- `runs/<cutlass_run>/ncu_profile.ncu-rep`

## Produce a compact comparison note

Create a short markdown note, for example:

- `todo/agent_input_snapshot.md`

Include:

- custom run dir
- CUTLASS run dir
- custom median runtime and TFLOP/s
- CUTLASS median runtime and TFLOP/s
- correctness status of both
- 3 to 6 notable NCU metric differences
- the concrete question for the next agent

## Concrete question for the next agent

Use this wording:

```text
Compare the latest custom kernel run against the latest CUTLASS baseline for fixed_bf16_gemm_v1. Based on summary.json, perf JSON, ncu_metrics.csv, docs/heuristics.md, and the current state files, propose exactly three optimization directions. For each direction, state the hypothesis, the bottleneck it targets, the code areas to change, the main risk, and the metrics to re-check after implementation.
```

## Definition of done

- both custom and CUTLASS run inputs are identified
- a compact markdown handoff note exists
- the next agent can work from structured files without needing raw terminal history

## Suggested prompt for VSCode chat

```text
Please complete todo/04_prepare_agent_inputs.md. Build a compact handoff package from the latest successful custom run and latest successful CUTLASS run, then write a markdown snapshot that another agent can use to propose exactly three optimization directions.
```
