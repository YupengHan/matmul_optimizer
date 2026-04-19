# State directory

The state layer now has two tiers:

1. machine-readable JSON for scripts and Codex
2. human-readable Markdown for review and hiring-manager readability

The two tiers should describe the same workflow state.

## Machine-readable files

## `graph_state.json`

Top-level workflow pointer.

Key fields:

- `current_node`: the next actionable node
- `previous_node`: the most recently completed node
- `status`: current workflow status
- `latest_run_dir`
- `latest_summary_json`
- `latest_ncu_summary_json`
- `latest_commit`
- `approved_direction_id`
- `recommended_direction_id`
- `current_kernel_path`
- `plateau_counter`
- `notes`

## `latest_run.json`

Latest lightweight summary from node_a.

Contains:

- run id / run dir
- kernel tag
- correctness summary
- performance summary
- references to raw run artifacts

## `latest_ncu_summary.json`

Latest lightweight Nsight Compute summary from node_a.

Contains:

- source run id
- kernel name
- block / grid shape
- registers / thread
- shared memory / block
- selected headline metrics

## `latest_diagnosis.json`

Node_b output.

Contains:

- source run references
- exactly 3 ranked directions
- one recommended direction

## `active_direction.json`

Node_c input.

Contains:

- selected direction id
- selection mode
- direction summary
- implementation status

## `benchmark_state.json`

Machine-readable baseline registry for:

- CUTLASS baseline
- best custom run

## `run_registry.jsonl`

Append-only lightweight log of node_a measurements.

## `round_loop_state.json`

Current multi-round loop budget and progress.

Contains:

- whether a loop is active
- total / completed / remaining rounds
- current or next round index
- whether recommended directions auto-select
- last completed round summary

## `round_history.jsonl`

Append-only one-line summary for each completed round.

## `supervisor_task.json`

Machine-readable dispatch contract for the main Codex supervisor.

Contains:

- which node should run next
- whether the main agent should run it directly or dispatch a `sub-agent`
- which protocol doc and context file to use
- which prepare / selection / finalize commands the main agent should run

## Human-readable files

## `latest_run.md`

Readable latest custom-run summary.

## `latest_ncu_summary.md`

Readable latest Nsight Compute snapshot.

## `progress.md`

High-level narrative progress and current graph status.

## `current_focus.md`

Small snapshot of the next action.

## `human_review.md`

Direction approval queue and node transition notes.

## `benchmark_baselines.md`

Readable benchmark snapshot and CUTLASS gap.

## `rounds.md`

Readable multi-round loop status and last completed round summary.

## `node_b_context.md`

Prepared read order and output contract for node_b.

## `node_c_context.md`

Prepared implementation brief and allowed edit surface for node_c.

## `supervisor_context.md`

Human-readable mirror of `supervisor_task.json` for the main Codex supervisor.

## Update rules

- node_a updates the latest run files, NCU files, graph state, progress, focus, and baselines
- node_a also closes the current round when it is measuring a just-implemented direction
- node_b updates diagnosis, review state, and graph state
- node_c updates active-direction state, build status, and graph state
- the supervisor view is refreshed whenever graph state or round-loop state changes
- raw logs belong under `runs/`, not under `state/`
