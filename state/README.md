# State directory

The state layer now has two tiers:

1. machine-readable JSON for scripts and LLM agents
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
- implemented direction provenance, including selection mode and idea origin
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
- optional `selected_direction_id` for later explicit selection
- `family_audit` notes about accepted, deferred, or rejected idea families
- candidate-style direction metadata such as family labels, fingerprints,
  numeric scores, and ranking notes

## `active_direction.json`

Node_c input.

Contains:

- selected direction id
- optional frontier candidate metadata such as `candidate_id`,
  `selected_from_frontier_id`, `family_id`, `subfamily_id`,
  `action_fingerprint`, `selection_priority`, and `base_run_id`
- selection mode
- direction summary
- implementation-edge annotations such as `implemented_action_fingerprint`,
  `semantic_delta_tags`, `secondary_family_ids`, and `actual_code_regions`
- implementation status

## `search_state.json`

Top-level heuristic-search scaffolding.

Contains:

- accepted measured base metadata
- best-known measured run metadata such as `best_known_run_id` and `best_known_runtime_ms`
- exact comparison-anchor metadata such as `exact_base_run_id` and `exact_base_runtime_ms`
- active frontier and candidate-set pointers
- last selected frontier candidate metadata
- last measured result metadata such as `last_result_run_id`, `last_result_runtime_ms`,
  `last_transition_label`, `last_result_registers_per_thread`, and
  `last_result_shared_mem_per_block_allocated`
- last restore metadata such as `last_restore_run_id`, `last_restore_source_commit`,
  `last_restore_at`, and `last_restore_reason`
- selection policy metadata
- latest-attempt pointer

## `search_frontier.json`

Persistent candidate frontier for structured candidate selection.

Contains:

- source run and latest diagnosis references
- selected candidate metadata
- candidate ranking notes and score breakdowns
- persistent historical candidate records
- family-representative metadata for the currently active search pool
- frontier items with `candidate_id`, `source_diagnosis_id`, `base_run_id`,
  `family_id`, `subfamily_id`, `action_fingerprint`, `priority`, and `status`
- one active representative candidate per family at a time
- optional reopen metadata such as `reopen_count`,
  `last_transition_label`, and `family_representative_score`

See also: `docs/search_policy.md` for the current reopen and family-reorder
policy.

## `search_closed.jsonl`

Append-only closed-set log for heuristic-search outcomes.

Entries are intended to record:

- which candidate was closed
- why it was closed
- which attempt or measured transition closed it
- score context at selection time
- measured runtime / correctness outcome and lightweight resource snapshot when node_a closes an attempt

## `family_ledger.json`

Coarse memory for direction families across rounds.

Contains:

- per-family aggregate counts such as `wins`, `flats`, `losses`, and `fails`
- last outcome label
- lightweight `freeze_status` such as `open`, `frozen`, or `closed_negative`
- best observed runtime within the family
- last measured resource snapshot for that family
- coarse prior notes for later scoring

## `search_candidates.json`

Normalized candidate projection of the latest finalized diagnosis.

Contains:

- candidate-set metadata
- recommended direction linkage
- exactly three candidate records projected from node_b directions
- fallback score fields plus explanatory notes
- family, subfamily, fingerprint, mode, gain prediction, and fail-risk fields

## `latest_attempt.json`

Current search-attempt bridge across selection, build, and later measurement.

Contains:

- selected candidate and direction metadata such as `candidate_id`,
  `source_diagnosis_id`, `base_run_id`, `family_id`, and `subfamily_id`
- planned-vs-implemented edge metadata such as `planned_action_fingerprint`,
  `implemented_action_fingerprint`, `semantic_delta_tags`,
  `secondary_family_ids`, and `actual_code_regions`
- implementation result metadata such as `build_status`, `failure_mode`,
  `diff_stats`, and nested build-log / touched-file fields
- commit metadata such as `commit`, `commit_short`, and `subject`
- later measurement-transition fields such as `transition_label` and measured
  headline metrics that node_a can fill only after a real run
- restore-base actions may also use this file, with `family_id=restore_base`,
  `mode=restore`, and `selection_mode=restore`

## `benchmark_state.json`

Machine-readable baseline registry for:

- CUTLASS baseline
- cuBLAS baseline
- best custom run

## `run_registry.jsonl`

Append-only lightweight log of node_a measurements.

Entries also record the implemented direction provenance for each measured run, including selection mode and idea origin.

`restore-base --run-id <run_id>` resolves its source commit from this log first
when possible, then falls back to the current latest/search-state pointers.

## `round_loop_state.json`

Current multi-round loop budget and progress.

Contains:

- whether a loop is active
- total / completed / remaining rounds
- current or next round index
- whether recommended directions auto-select
- whether frontier top candidates auto-select
- last completed round summary

## `round_history.jsonl`

Append-only one-line summary for each completed round.

Round entries record the selected direction, selection mode, and idea origin so regressed human-guided experiments remain traceable even when a later round restores an earlier baseline.

## `diagnosis_history.jsonl`

Append-only snapshot of every finalized node_b diagnosis, including all three directions, the recommended choice, and any round-specific diagnosis notes.

Directions may also carry an `idea_origin` field such as `human-idea` when a round is explicitly driven by user input rather than node_b analysis.

## `supervisor_task.json`

Machine-readable dispatch contract for the main LLM supervisor.

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

Human-readable mirror of `supervisor_task.json` for the main LLM supervisor.

## Update rules

- node_a updates the latest run files, NCU files, graph state, progress, focus, and baselines
- node_a also closes the current round when it is measuring a just-implemented direction
- node_b updates diagnosis, review state, and graph state
- node_c updates active-direction state, build status, and graph state
- the supervisor view is refreshed whenever graph state or round-loop state changes
- raw logs belong under `runs/`, not under `state/`
