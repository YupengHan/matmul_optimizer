# Heuristic Search Dataset

This folder is a structured history export for the BF16 GEMM optimization loop.

The goal is to support the next step of the project: moving from an informal
"try the next promising idea" workflow toward a more explicit heuristic or
A*-style search loop.

Instead of keeping the search history only in commit messages, run directories,
and ad hoc notes, this dataset turns each optimization cycle into machine-
readable records that can be ranked, filtered, summarized, and later used for
heuristic construction.

## What Is Collected

The dataset intentionally keeps both wins and failures.

Each record preserves:

- the parent measured state that triggered a diagnosis
- the three candidate directions proposed at `node_b`
- the one direction that was actually implemented at `node_c`
- the code locations and touched files for that implementation
- the real measurement result from `node_a`
- the profiler headline metrics and their deltas vs the previous measured run
- side effects that did not help runtime, because those are useful heuristic
  signals too

That means a later heuristic function can learn from patterns such as:

- a runtime improvement that came with worse DRAM pressure
- a long-scoreboard reduction that still regressed total runtime
- a family of ideas that repeatedly looked plausible but closed negative

## Files

- `build_dataset.py`
  Reads git history plus local `runs/*/summary.json` and
  `runs/*/ncu_summary.json`, then refreshes the exported snapshot files.
- `manifest.json`
  Small generation summary pinned to the exact `HEAD` commit used for the
  export.
- `diagnoses.jsonl`
  One JSON object per `node_b` diagnosis commit. This is the "search state plus
  candidate actions" view.
- `attempts.jsonl`
  One JSON object per `node_c` implementation attempt. This is the
  "state -> action -> next measured state" view.

## Record Shapes

`diagnoses.jsonl` focuses on branching:

- `source_run_id`
- `family_audit`
- `recommended_direction_id`
- `directions[]` with `hypothesis`, `expected_bottleneck`, `code_locations`,
  `risk`, `metrics_to_recheck`, and when available:
  `family_id`, `subfamily_id`, `action_fingerprint`, `mode`,
  `search_score_v1`, `score_breakdown`, `predicted_gain_ms`,
  `predicted_fail_risk`, and `ranking_notes`
- `selected_direction_id`
- `selected_implementation_commit`

`attempts.jsonl` focuses on transitions:

- `parent_state_run_id`
- `candidate_id`
- `base_run_id`
- `family_id` / `subfamily_id`
- `planned_action_fingerprint`
- `implemented_action_fingerprint`
- `transition_label`
- `semantic_delta_tags`
- `resource_snapshot`
- `family_status` / `family_ledger_snapshot` when available
- `action.direction_id`
- `action.direction_name`
- `action.motivation`
- `implementation.commit`
- `implementation.parent_commit`
- `implementation.touched_files`
- `implementation.diff_stats`
- `result_state.run_id`
- `result_state.runtime_ms`
- `result_state.runtime_delta_ms`
- `result_state.headline_metrics`
- `result_state.headline_metric_deltas_vs_previous_run`

## Why JSONL

JSONL keeps each optimization event as one independent row, which makes it easy
to:

- load the history into pandas, DuckDB, or SQLite
- group by idea family or bottleneck class
- compare profiler deltas for improvements vs regressions
- build future heuristic features without reparsing commit text

## Data Sources

The export is built from the existing local workflow instead of inventing a new
parallel tracking system.

Primary sources:

- `node_b` commits and their committed `state/latest_diagnosis.json`
- `node_c` commits and their implementation commit messages
- `node_a` commits and their measurement commit messages
- local run artifacts under `runs/*/summary.json`
- local run artifacts under `runs/*/ncu_summary.json`
- committed search-memory snapshots such as `state/latest_attempt.json` and
  `state/family_ledger.json` when they exist in the relevant historical commit

Large artifacts are not duplicated here. The dataset stores stable references
such as commit SHAs, run IDs, and local artifact paths so later analysis can
pull raw detail on demand.

## Backward Compatibility

The exporter is intentionally additive.

- new search-oriented fields support heuristic search and best-first selection
- older history may not have committed `family_id`, fingerprints, scores,
  `latest_attempt.json`, or `family_ledger.json`
- when those fields are missing in old commits, the exporter keeps the row and
  emits `null`, empty structures, or deterministic fallback values where that is
  safe

This is why the dataset still uses `schema_version = 1`: the export shape gained
optional fields, but the old rows and old generation flow remain valid.

## Refresh

Run:

```bash
python heuristic_dataset/build_dataset.py
```

The script only reads git history and local run summaries, then rewrites the
snapshot files inside this folder.
