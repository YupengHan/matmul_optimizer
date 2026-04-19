# matmul_optimizer

Shape-specialized, script-first CUDA kernel optimization for one fixed BF16 GEMM on a single RTX 3070 Laptop GPU.

## Goal

This repo is intentionally narrow:

- benchmark one fixed BF16 GEMM shape
- optimize a custom CUDA kernel for that exact shape
- measure correctness, runtime, and Nsight Compute data locally
- use Codex as a diagnosis / implementation agent inside a reproducible workflow
- beat the local CUTLASS baseline on this fixed shape

The workflow is now a lightweight, LangGraph-inspired loop:

```text
node_a -> node_b -> node_c -> node_a
```

It borrows only the concepts of nodes, edges, and state. It does **not** depend on LangGraph, OpenAI API keys, or any cloud runtime.

Codex now has an explicit supervisor layer above that loop:

- the main Codex agent owns graph dispatch and loop control
- `node_a` stays direct and script-first
- `node_b` and `node_c` are intended to run through one Codex `sub-agent` each
- the repo exposes the dispatch contract through `state/supervisor_task.json` and `docs/supervisor_protocol.md`

## Fixed benchmark target

`fixed_bf16_gemm_v1`

- `m = 6464`
- `n = 7776`
- `k = 7232`
- all dims are multiples of 32
- none are multiples of 128
- BF16 inputs
- FP32 reference accumulation
- BF16 output reference also stored

## What is script-first vs agent-driven

Script-first:

- dataset generation
- configure / build
- kernel evaluation
- Nsight Compute capture
- machine-readable state updates
- lightweight state commits

Codex-friendly agent nodes:

- `node_b`: diagnose the latest measured run and output exactly three directions
- `node_c`: implement one selected direction, prove the code still builds, then hand back to `node_a`

Supervisor-only orchestration:

- the main agent reads `state/supervisor_task.json`
- it decides whether to run a node directly or dispatch a `sub-agent`
- it always runs the finalize command after a `sub-agent` returns

## Repository layout

```text
matmul_optimizer/
├── AGENTS.md
├── README.md
├── CMakeLists.txt
├── .gitignore
├── .gitmessage
├── configs/
│   ├── fixed_bf16_gemm_v1.json
│   └── ncu_metrics_core.txt
├── docs/
│   ├── commit_convention.md
│   ├── heuristics.md
│   ├── node_b_protocol.md
│   ├── node_c_protocol.md
│   ├── supervisor_protocol.md
│   └── pipeline_graph.md
├── include/
├── scripts/
│   ├── eval_kernel.py
│   ├── generate_fixed_bf16_dataset.py
│   ├── graph.py
│   ├── run_cutlass_baseline.py
│   └── state_lib.py
├── src/
│   ├── kernels/
│   └── runner/
├── state/
│   ├── README.md
│   ├── graph_state.json
│   ├── latest_run.json
│   ├── latest_ncu_summary.json
│   ├── latest_diagnosis.json
│   ├── active_direction.json
│   ├── benchmark_state.json
│   ├── latest_run.md
│   ├── latest_ncu_summary.md
│   ├── progress.md
│   ├── current_focus.md
│   ├── human_review.md
│   ├── benchmark_baselines.md
│   ├── round_loop_state.json
│   ├── round_history.jsonl
│   ├── node_b_context.md
│   ├── node_c_context.md
│   ├── supervisor_task.json
│   └── supervisor_context.md
├── artifacts/
└── runs/
```

## Main-loop commands

Generate the fixed dataset once:

```bash
python scripts/generate_fixed_bf16_dataset.py
```

Inspect workflow state:

```bash
python scripts/graph.py status
python scripts/graph.py supervisor
```

Run the current actionable node from `state/graph_state.json`:

```bash
python scripts/graph.py cycle
```

Inspect or arm a multi-round loop:

```bash
python scripts/graph.py rounds --status
python scripts/graph.py rounds --count 5 --auto-use-recommended
```

Run the fully script-first measurement node:

```bash
python scripts/graph.py node_a
```

Prepare node_b context:

```bash
python scripts/graph.py node_b
```

After Codex writes exactly three directions into `state/latest_diagnosis.json`, finalize node_b:

```bash
python scripts/graph.py node_b --finalize
```

Select a direction:

```bash
python scripts/graph.py approve --direction dir_02
```

or continue with the recommended direction:

```bash
python scripts/graph.py use-recommended-direction
```

Prepare node_c:

```bash
python scripts/graph.py node_c
```

After editing code for exactly one direction, finalize node_c:

```bash
python scripts/graph.py node_c --finalize
```

By default, node_c finalize auto-runs node_a, which closes the loop.

## Multi-round workflow

The repo now supports a round budget for Codex-driven optimization loops.

Example:

```bash
python scripts/graph.py rounds --count 5 --auto-use-recommended
```

This means:

- plan 5 rounds
- each round is `node_b -> node_c -> node_a`
- the main Codex agent stays in charge for the whole loop
- `node_b` and `node_c` can each use one dedicated `sub-agent`
- `--auto-use-recommended` is the explicit low-human-friction flag that allows the loop to keep moving with the rank-1 direction
- each completed round is appended to `state/round_history.jsonl`
- current loop status lives in `state/round_loop_state.json`
- current supervisor dispatch lives in `state/supervisor_task.json`
- human-readable loop status lives in `state/rounds.md`

The round-level performance record is written by the `node_a:` commit after the re-measurement step. That commit now carries:

- the implementation idea / hypothesis
- runtime delta vs the previous measured run
- TFLOP/s delta
- the run directory
- the Nsight Compute summary path
- the `.ncu-rep` path

## Build behavior

The main loop should not depend on CUTLASS.

Main-loop configure/build:

```bash
cmake -S . -B build -DENABLE_CUTLASS_RUNNER=OFF
cmake --build build -j 4 --target custom_runner
```

This keeps `node_a` and `node_c` from blocking on CUTLASS setup or network fetches.

## CUTLASS baseline is a side node

CUTLASS remains part of the repo, but it is intentionally off the main loop.

To build the baseline runner:

```bash
cmake -S . -B build -DENABLE_CUTLASS_RUNNER=ON -DCUTLASS_ROOT=/path/to/cutlass
cmake --build build -j 4 --target cutlass_runner
```

To record a CUTLASS baseline run:

```bash
python scripts/run_cutlass_baseline.py \
  --runner ./build/cutlass_runner \
  --kernel-tag cutlass_ref_v1
```

Use CUTLASS as:

- the target to beat
- a periodic refresh point after plateaus
- a comparison source for NCU differences

Do **not** let CUTLASS setup block the main custom-kernel loop.

## Current workflow semantics

### main supervisor

- reads `state/supervisor_task.json`
- dispatches `node_a` directly
- dispatches `node_b` and `node_c` through one `sub-agent` each
- runs finalize commands after `sub-agent` completion
- re-reads graph state before starting the next node

Repo-local Python prepares and validates this handoff, but does **not** try to spawn Codex agents itself.

### node_a

- builds `custom_runner` when needed
- runs `scripts/eval_kernel.py`
- writes raw run artifacts under `runs/`
- writes lightweight summaries under `state/`
- updates graph state to point at `node_b`
- creates a `node_a:` commit with state only

### node_b

- reads the latest lightweight summaries, heuristics, kernel, and state
- normally runs inside one diagnosis `sub-agent`
- outputs exactly 3 ranked directions
- updates review state and graph state
- creates a `node_b:` commit with state only
- points the workflow at `node_c`

### node_c

- reads the selected direction
- normally runs inside one implementation `sub-agent`
- implements exactly one direction
- proves the build still passes
- creates a `node_c:` commit only after build success
- auto-runs `node_a` by default

## State model

Machine-readable:

- `state/graph_state.json`
- `state/latest_run.json`
- `state/latest_ncu_summary.json`
- `state/latest_diagnosis.json`
- `state/active_direction.json`
- `state/benchmark_state.json`
- `state/run_registry.jsonl`
- `state/round_loop_state.json`
- `state/round_history.jsonl`
- `state/supervisor_task.json`

Human-readable:

- `state/latest_run.md`
- `state/latest_ncu_summary.md`
- `state/progress.md`
- `state/current_focus.md`
- `state/human_review.md`
- `state/benchmark_baselines.md`
- `state/rounds.md`
- `state/node_b_context.md`
- `state/node_c_context.md`
- `state/supervisor_context.md`

## Git and artifact policy

Commit:

- lightweight state
- code changes
- docs / protocol changes

Do not commit:

- `runs/`
- `artifacts/` dataset binaries
- `build/`
- `*.ncu-rep`
- raw NCU CSV/log files

Commit categories:

- `node_a:`
- `node_b:`
- `node_c:`

See:

- `AGENTS.md`
- `docs/commit_convention.md`
- `.gitmessage`

## Where Codex should look first

If you are operating this repo through Codex CLI, start with:

1. `AGENTS.md`
2. `python scripts/graph.py status`
3. `python scripts/graph.py supervisor`
4. the protocol doc for the current node:
   - `docs/supervisor_protocol.md`
   - `docs/node_b_protocol.md`
   - `docs/node_c_protocol.md`
