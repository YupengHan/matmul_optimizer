# Pipeline graph

This repo uses a lightweight, LangGraph-inspired workflow:

```text
dataset_init -> node_a -> node_b -> node_c -> node_a
```

Only the state / node / edge idea is borrowed. The execution path stays local and script-first.

LLM agents now operate this graph through a small supervisor layer:

- the main LLM agent owns graph dispatch
- `node_a` is executed directly
- `node_b` and `node_c` are dispatched to one `sub-agent` each
- the repo exposes the current dispatch through `state/supervisor_task.json`

## Design principles

- execution-critical steps stay in scripts
- reasoning-heavy steps are LLM-friendly agent nodes
- the main LLM agent remains the supervisor and finalize owner
- machine-readable state and human-readable state are both required
- git is the audit log for measured runs, diagnoses, and implementations
- optional multi-round loop state can budget repeated node_b -> node_c -> node_a rounds
- CUTLASS is a side-path baseline node, not part of the main loop

## Graph sketch

```mermaid
flowchart TD
    SUP[main LLM supervisor] --> D0[dataset_init script]
    SUP --> A[node_a script]
    SUP --> B[node_b diagnosis sub-agent]
    SUP --> SEL[approve or use recommended direction]
    SUP --> C[node_c implementation sub-agent]
    A --> B
    B --> SEL
    SEL --> C
    C --> A

    A -. optional baseline refresh .-> CUTLASS[run_cutlass_baseline script]
    CUTLASS -. update benchmark state .-> B

    B -. optional later extension .-> OUTBOX[outbox thinking]
```

## Node semantics

## `dataset_init`

One-time or rare setup node.

Responsibilities:

- generate the fixed dataset
- populate `artifacts/datasets/fixed_bf16_gemm_v1/`

## `node_a`

The fully script-first measurement node.

Responsibilities:

- run outside the LLM sandbox so CUDA benchmarking and Nsight Compute can reach the GPU
- build `custom_runner` if needed
- run `scripts/eval_kernel.py`
- record correctness / performance / Nsight Compute
- keep raw artifacts under `runs/`
- write lightweight summaries under `state/`
- update `state/graph_state.json` so the next node is `node_b`
- create a `node_a:` commit with lightweight state only

Key outputs:

- `state/latest_run.json`
- `state/latest_ncu_summary.json`
- `state/latest_run.md`
- `state/latest_ncu_summary.md`
- `state/graph_state.json`

## `node_b`

The diagnosis node.

Responsibilities:

- run under the main LLM supervisor as one diagnosis `sub-agent`
- read the latest lightweight run summary
- read the latest lightweight NCU summary
- read `docs/heuristics.md`
- read the current kernel
- output exactly 3 optimization directions
- set one `recommended_direction_id`
- update graph state so the workflow points at `node_c`
- create a `node_b:` commit with lightweight state only

Key outputs:

- `state/latest_diagnosis.json`
- `state/human_review.md`
- `state/node_c_context.md`
- `state/supervisor_task.json`

## `node_c`

The implementation node.

Responsibilities:

- run under the main LLM supervisor as one implementation `sub-agent`
- read the selected direction
- implement exactly one direction
- build before claiming success
- stop and update failure state if the build fails
- commit code plus lightweight state after build success
- auto-run `node_a` by default

Guardrails:

- one direction per loop
- no automatic merge
- no performance claim before node_a re-measures

## Side nodes: `run_cutlass_baseline` and `run_cublas_baseline`

Responsibilities:

- measure the CUTLASS or cuBLAS reference path on the same dataset
- refresh the benchmark target
- update benchmark state and human-readable baseline notes

This node is intentionally **off the execution-critical path**.

## State model

## Machine-readable state

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

## Human-readable state

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

The two layers must not contradict each other.

## Supervisor state

The extra orchestration layer is explicit rather than implicit.

`state/supervisor_task.json` tells the main LLM agent:

- which node to dispatch next
- whether to run it directly or through a `sub-agent`
- which protocol doc to use
- which prepare / selection / finalize commands to run
- when the next 5-round context/display maintenance checkpoint lands
- whether the 10-minute idle watchdog has emitted a continue instruction

`state/supervisor_context.md` is the human-readable mirror of that dispatch state.

## Git as workflow memory

Git commit classes:

- `node_a:` measured state
- `node_b:` diagnosis state
- `node_c:` implementation after build success

When a multi-round loop is active, the node commits should carry the round label, and the node_a commit should record:

- modification idea
- runtime delta
- TFLOP/s delta
- run dir
- profile paths

This keeps the workflow auditable without committing raw artifacts.

## Outbox thinking

Outbox thinking remains intentionally small in this retrofit.

Keep it as a later extension for:

- branch-heavy exploration
- larger architectural rewrites
- ideas that should not enter the main loop immediately
