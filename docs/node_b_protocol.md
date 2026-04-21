# Node B protocol

Node B is the diagnosis node. It does not call a remote model from inside `scripts/graph.py`; Codex performs the reasoning step after the repo prepares the context.

In the intended workflow, Node B is executed by one diagnosis `sub-agent` under the main Codex supervisor.

## Entry

Prepare the context with:

```bash
python scripts/graph.py node_b
```

Finalize the diagnosis with:

```bash
python scripts/graph.py node_b --finalize
```

The main Codex supervisor is responsible for both commands. The `sub-agent` owns only the reasoning and the edit to `state/latest_diagnosis.json`.

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

The supervisor should also read:

- `docs/supervisor_protocol.md`
- `state/supervisor_task.json`

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
- `family_audit`
- `selected_direction_id`
- `directions`

`directions` must contain exactly 3 items. Each item must contain:

- `direction_id`
- `rank`
- `name`
- `family_id`
- `subfamily_id`
- `action_fingerprint`
- `mode`
- `hypothesis`
- `expected_bottleneck`
- `code_locations`
- `risk`
- `metrics_to_recheck`
- `search_score_v1`
- `score_breakdown`
- `predicted_gain_ms`
- `predicted_fail_risk`
- `ranking_notes`
- `stop_condition`

The top-level `notes` field should be used when useful to record human-guided ranking rationale.
The top-level `family_audit` field should remain a list and can summarize which idea families were accepted, deferred, or rejected this round.
`selected_direction_id` may remain `null` at diagnosis time because finalize now emits candidates into the frontier without automatically selecting one.

## Direction quality bar

The three directions should be materially different. Do not submit three small variants of the same idea.

The recommended direction should be the best expected upside / implementation-risk tradeoff for the next loop.

Each direction is also a search candidate.

That means each direction should carry:

- stable family labels
- a deterministic or auditable action fingerprint
- a coarse numeric score
- prose notes that explain why the score is what it is

Do not fake precision. Keep the numeric score coarse and use `ranking_notes` to preserve the reasoning that a later fuzzy reranker may need.

From round 5 onward, diagnosis must also explicitly reflect the user-provided human ideas from `state/human_review.md` instead of treating them as soft background context only.

That reflection must:

- review the listed idea families one by one against the latest measured evidence
- say which ideas are being accepted, deferred, or rejected for this round
- choose one primary idea family for the recommended direction
- explain why the measured evidence makes that family the next best move

The three directions do not need extra schema fields for this, but their `hypothesis` text and the diagnosis `notes` should make the mapping auditable.

## State updates

`python scripts/graph.py node_b --finalize` will:

- validate that there are exactly 3 directions
- backfill deterministic `action_fingerprint` and `search_score_v1` fields when they are omitted
- project all 3 directions into `state/search_candidates.json`
- enqueue all 3 directions as open frontier items in `state/search_frontier.json`
- set `state/graph_state.json` to point at `node_c`
- refresh `state/current_focus.md`, `state/progress.md`, `state/human_review.md`
- prepare `state/node_c_context.md`
- create the node_b git commit unless `--skip-commit` is passed

If a multi-round loop is active with `--auto-use-recommended`, finalize also auto-selects the recommended direction so node_c can start immediately.

## Sub-agent boundary

The diagnosis `sub-agent` should:

- read the required inputs
- edit only lightweight state for the diagnosis
- avoid running the finalize command by itself

After the `sub-agent` returns, the main Codex supervisor must run:

```bash
python scripts/graph.py node_b --finalize
```

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
