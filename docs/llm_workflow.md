# LLM Workflow Guide

This document keeps LLM-operator details out of the public-facing `README.md`.

Use it as the quick entrypoint when you are running the optimization loop locally through an LLM CLI or another coding agent.

## Read Order

Start here:

1. [AGENTS.md](../AGENTS.md)
2. `python scripts/graph.py status`
3. `python scripts/graph.py supervisor`
4. [docs/supervisor_protocol.md](supervisor_protocol.md)
5. the node-specific protocol for the current task:
   - [docs/node_b_protocol.md](node_b_protocol.md)
   - [docs/node_c_protocol.md](node_c_protocol.md)
6. [state/README.md](../state/README.md)
7. `state/supervisor_task.json` and `state/supervisor_context.md`

`README.md` is now for humans first. Do not treat it as the operator manual.

## Standard Commands

Generate the fixed dataset:

```bash
python scripts/generate_fixed_bf16_dataset.py
```

Inspect workflow state:

```bash
python scripts/graph.py status
python scripts/graph.py supervisor
```

Rebootstrap a fresh refactor/search branch from a measured implementation baseline:

```bash
python scripts/graph.py rebootstrap --baseline-run-id 20260420_235922_bf16_gemm_v1_489574e --goal-runtime-ms 18 --goal-competitor cuBLAS
```

Run the measurement node directly:

```bash
python scripts/graph.py node_a
```

Prepare and finalize diagnosis:

```bash
python scripts/graph.py node_b
python scripts/graph.py node_b --finalize
```

Select a direction:

```bash
python scripts/graph.py approve --direction dir_02
python scripts/graph.py use-recommended-direction
```

Prepare and finalize implementation:

```bash
python scripts/graph.py node_c
python scripts/graph.py node_c --finalize
```

Drive a multi-round loop:

```bash
python scripts/graph.py rounds --status
python scripts/graph.py rounds --count N
```

Optional CUTLASS side-path:

```bash
cmake -S . -B build -DENABLE_CUTLASS_RUNNER=ON -DCUTLASS_ROOT=/path/to/cutlass
cmake --build build -j 4 --target cutlass_runner
python scripts/run_cutlass_baseline.py --runner ./build/cutlass_runner --kernel-tag cutlass_ref_v1
```

Optional cuBLAS side-path:

```bash
cmake -S . -B build -DENABLE_CUBLAS_RUNNER=ON
cmake --build build -j 4 --target cublas_runner
python scripts/run_cublas_baseline.py --runner ./build/cublas_runner --kernel-tag cublas_ref_v1
```

## Execution Model

The workflow is:

```text
node_a -> node_b -> node_c -> node_a
```

The supervisor contract is explicit:

- the main agent reads `state/supervisor_task.json`
- `node_a` runs directly and remains script-first
- `node_b` uses one diagnosis sub-agent
- `node_c` uses one implementation sub-agent
- the main agent always runs the finalize command after a sub-agent returns
- after every node completion, the main agent re-reads `state/supervisor_task.json`

Deeper semantics live in:

- [docs/supervisor_protocol.md](supervisor_protocol.md)
- [docs/pipeline_graph.md](pipeline_graph.md)
- [AGENTS.md](../AGENTS.md)

## State Files

The state layer has two tiers:

- machine-readable JSON for scripts and agents
- human-readable Markdown for review and workflow handoff

Use [state/README.md](../state/README.md) as the file-level reference.

The most important files during active operation are:

- `state/graph_state.json`
- `state/supervisor_task.json`
- `state/latest_run.json`
- `state/latest_ncu_summary.json`
- `state/latest_diagnosis.json`
- `state/active_direction.json`
- `state/progress.md`
- `state/current_focus.md`

## Related Docs

- [docs/benchmark_spec.md](benchmark_spec.md): fixed benchmark definition
- [docs/commit_convention.md](commit_convention.md): commit structure for `node_a`, `node_b`, and `node_c`
- [docs/heuristics.md](heuristics.md): diagnosis heuristics for node_b
- [state/README.md](../state/README.md): update rules for the state layer
