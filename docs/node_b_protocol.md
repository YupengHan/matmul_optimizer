# Node B protocol

Node B is the diagnosis node. It does not call a remote model from inside `scripts/graph.py`; Codex performs the reasoning step after the repo prepares the context.

## Entry

Prepare the context with:

```bash
python scripts/graph.py node_b
```

Finalize the diagnosis with:

```bash
python scripts/graph.py node_b --finalize
```

## Required inputs

Read these in order:

1. `state/node_b_context.md`
2. `state/latest_run.md`
3. `state/latest_ncu_summary.md`
4. `docs/heuristics.md`
5. `state/progress.md`
6. `state/current_focus.md`
7. `state/human_review.md`
8. current kernel source
9. raw run files referenced from `state/node_b_context.md`

## Required output

Edit `state/latest_diagnosis.json`.

It must contain:

- `diagnosis_id`
- `status`
- `source_run_id`
- `source_run_dir`
- `source_summary_json`
- `source_ncu_summary_json`
- `current_kernel_path`
- `recommended_direction_id`
- `directions`

`directions` must contain exactly 3 items. Each item must contain:

- `direction_id`
- `rank`
- `name`
- `hypothesis`
- `expected_bottleneck`
- `code_locations`
- `risk`
- `metrics_to_recheck`
- `stop_condition`

## Direction quality bar

The three directions should be materially different. Do not submit three small variants of the same idea.

The recommended direction should be the best expected upside / implementation-risk tradeoff for the next loop.

## State updates

`python scripts/graph.py node_b --finalize` will:

- validate that there are exactly 3 directions
- set `state/graph_state.json` to point at `node_c`
- refresh `state/current_focus.md`, `state/progress.md`, `state/human_review.md`
- prepare `state/node_c_context.md`
- create the node_b git commit unless `--skip-commit` is passed

If a multi-round loop is active with `--auto-use-recommended`, finalize also auto-selects the recommended direction so node_c can start immediately.

## Commit rule

Node B commits state only. Do not commit raw `runs/` files or heavyweight artifacts.

The commit must be auditable and should explain:

- which measured run was diagnosed
- which direction is recommended
- what the three direction names are

## Human-in-loop rule

Preferred path:

- explicit approval via `python scripts/graph.py approve --direction dir_0X`

Low-friction path:

- `python scripts/graph.py use-recommended-direction`

Either path should happen before node_c edits code.
