# Heuristic Search Refactor Plan

This document is a long-lived planning reference for evolving the current
`node_b -> node_c -> node_a` loop into a more structured heuristic-search
workflow.

It is intentionally a spec and sequencing document, not an implementation
patch. The repo must remain script-first and fixed-benchmark-first.

## Background And Goal

This repository optimizes one fixed BF16 GEMM benchmark:

- shape: `m=6464, n=7776, k=7232`
- dtype: BF16 inputs, FP32 accumulation, BF16 output reference
- target: beat the local CUTLASS baseline on `fixed_bf16_gemm_v1`

The goal is not to build a general autotuning framework.

The goal is to keep the current measured workflow intact while upgrading the
current experience-driven loop into a more explicit heuristic search:

```text
measured state -> candidate directions -> one selected attempt -> measured result
```

The current loop already has the right operational shape:

```text
node_a -> node_b -> node_c -> node_a
```

The refactor should preserve that loop while making the search state more
explicit, auditable, and reusable across Codex sessions.

## Current System Summary

### Supervisor

The main Codex agent is the supervisor.

- reads `state/supervisor_task.json`
- runs `node_a` directly
- prepares `node_b` and `node_c`, then dispatches exactly one sub-agent for each
- runs finalize commands after sub-agent work returns
- keeps multi-round loops running until the loop budget is exhausted or the
  graph pauses

### `node_a`

`node_a` is the only real measurement node.

- builds `custom_runner` if needed
- runs `scripts/eval_kernel.py`
- records correctness, runtime, TFLOP/s, and Nsight Compute outputs
- updates the latest measured state and append-only run history
- closes a round when a just-implemented direction is re-measured

Any search refactor must keep `node_a` as the only place that can claim
performance.

### `node_b`

`node_b` is the diagnosis node.

- consumes the latest measured run plus heuristics context
- writes `state/latest_diagnosis.json`
- must emit exactly 3 directions
- must set one `recommended_direction_id`
- currently produces human-readable diagnosis text, but does not yet emit a
  first-class search frontier record

### `node_c`

`node_c` is the implementation node.

- consumes exactly one selected direction via `state/active_direction.json`
- edits code for exactly one direction
- must pass build validation in `python scripts/graph.py node_c --finalize`
- hands control back to `node_a`

Any search refactor must keep `node_c` scoped to one selected attempt at a
time.

### Current State Files

Current machine-readable state already covers:

- graph position: `state/graph_state.json`
- supervisor dispatch: `state/supervisor_task.json`
- latest measured run: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- latest diagnosis: `state/latest_diagnosis.json`
- selected direction for implementation: `state/active_direction.json`
- round-loop tracking: `state/round_loop_state.json`
- measurement and diagnosis history: `run_registry.jsonl`,
  `round_history.jsonl`, `diagnosis_history.jsonl`

What is missing is explicit search state:

- frontier candidates separated from human diagnosis prose
- closed-set attempt records in a search-native schema
- family-level memory of which idea families are live, plateaued, or closed
- a latest-attempt bridge between `node_c` build success and `node_a`
  transition classification

## Refactor Principles

- Keep the execution-critical path script-first.
- Keep `node_a` as the only measurement authority.
- Keep `node_b` at exactly 3 directions.
- Keep `node_c` at exactly one selected direction.
- Add state additively before changing selection behavior.
- Prefer coarse, auditable heuristics over fake precision.
- Store both numeric scores and explanation fields such as
  `score_breakdown` and `ranking_notes`.
- Stay fixed-shape-first; do not generalize the benchmark definition.

## Planned Phases

### Phase 1

State scaffolding + `node_b` candidate emission + frontier selection MVP.

Intent:

- introduce first-class search state files without replacing existing state
- normalize the 3 `node_b` directions into candidate records
- select one next attempt from a frontier record instead of relying only on
  `recommended_direction_id`

Expected behavior boundary:

- `node_b` still outputs exactly 3 directions in `latest_diagnosis.json`
- `node_c` still implements exactly one selected direction
- `node_a` remains the only measured transition
- selection can stay conservative and fall back to the current recommendation

### Phase 2

`latest_attempt` + `node_a` transition classification + family ledger +
restore-base support.

Intent:

- record the active search attempt as its own object
- classify the measured result of an attempt in `node_a`
- add family-level memory so repeated dead-end families can be deprioritized
- make restore-to-accepted-base a first-class search transition instead of only
  an operational recovery tool

Expected behavior boundary:

- still one implementation attempt per `node_c`
- still one measured result per `node_a`
- no automatic multi-attempt branching inside a single loop

### Phase 3

`heuristic_dataset` export extension + stronger scoring.

Intent:

- export the new search-native fields into the dataset snapshot
- preserve backward-readable history while adding search metadata
- strengthen selection scoring with more evidence from attempt history and
  family history

Expected behavior boundary:

- the search remains heuristic-driven, not a full online planner
- missing history must still degrade gracefully to a simple fallback score

## New State Files

### `state/search_state.json`

Global search-session state for the current measured anchor and currently chosen
search mode.

Primary use:

- records the accepted measured base
- points to the active frontier
- records the current search iteration
- stores high-level search mode and notes

Schema draft:

```json
{
  "schema_version": 1,
  "status": "idle",
  "search_mode": "heuristic_mvp",
  "search_iteration": 0,
  "accepted_base_run_id": null,
  "accepted_base_measured_commit": null,
  "accepted_base_runtime_ms": null,
  "active_frontier_id": null,
  "active_candidate_set_id": null,
  "active_candidate_id": null,
  "latest_attempt_id": null,
  "last_transition_type": null,
  "selection_policy": {
    "policy_id": "heuristic_v1_fallback",
    "allow_restore_base": true,
    "max_open_candidates": 3
  },
  "notes": "Search state is idle until a measured base is available."
}
```

### `state/search_frontier.json`

Current open frontier for the next selection step.

Primary use:

- stores the normalized candidate records emitted from the latest diagnosis
- stores ranking metadata separate from human diagnosis prose
- stores exactly one selected candidate for `node_c`

Schema draft:

```json
{
  "schema_version": 1,
  "frontier_id": null,
  "status": "empty",
  "source_run_id": null,
  "source_measured_commit": null,
  "source_diagnosis_id": null,
  "candidate_set_id": null,
  "generated_at": null,
  "selection_policy_id": "heuristic_v1_fallback",
  "selected_candidate_id": null,
  "selection_reason": null,
  "selection_summary": null,
  "candidates": [
    {
      "candidate_id": "cand_01",
      "direction_id": "dir_01",
      "direction_rank": 1,
      "direction_name": null,
      "family_id": null,
      "parent_run_id": null,
      "parent_commit": null,
      "selection_state": "open",
      "fallback_score": null,
      "score_breakdown": {},
      "ranking_notes": [],
      "hypothesis": null,
      "expected_bottleneck": null,
      "code_locations": [],
      "risk": null,
      "metrics_to_recheck": [],
      "provenance": {
        "diagnosis_id": null,
        "selection_mode_hint": "recommended_or_manual"
      }
    }
  ],
  "notes": "Phase 1 MVP keeps only the current open frontier."
}
```

### `state/search_closed.jsonl`

Append-only log of closed search items.

Primary use:

- records attempted candidates
- records candidates explicitly skipped or superseded
- records restore-base transitions as search-native events

Schema draft for one line:

```json
{
  "schema_version": 1,
  "closed_at": null,
  "search_iteration": null,
  "candidate_id": null,
  "frontier_id": null,
  "parent_run_id": null,
  "family_id": null,
  "close_reason": "measured_regression",
  "close_reason_detail": null,
  "attempt_id": null,
  "measurement_run_id": null,
  "runtime_delta_ms": null,
  "correctness": null,
  "score_at_selection": null,
  "score_breakdown": {},
  "ranking_notes": [],
  "notes": null
}
```

### `state/family_ledger.json`

Coarse memory for idea families across rounds.

Primary use:

- groups attempts by family instead of only by direction id
- prevents the search from forgetting repeated regressions
- stores simple family-level priors for future selection

Schema draft:

```json
{
  "schema_version": 1,
  "updated_at": null,
  "families": {
    "ptx_export_cleanup": {
      "family_label": "PTX export cleanup",
      "status": "live",
      "attempt_count": 0,
      "measured_count": 0,
      "improved_count": 0,
      "regressed_count": 0,
      "build_failed_count": 0,
      "last_attempt_id": null,
      "last_run_id": null,
      "best_runtime_ms": null,
      "best_run_id": null,
      "last_outcome_class": null,
      "coarse_prior": 0.0,
      "notes": []
    }
  }
}
```

### `state/search_candidates.json`

Normalized candidate set emitted from `node_b`.

Primary use:

- keeps a machine-friendly candidate projection of the 3 diagnosis directions
- allows future scoring or reranking without reparsing prose from
  `latest_diagnosis.json`
- preserves explanation fields next to numeric scores

Schema draft:

```json
{
  "schema_version": 1,
  "candidate_set_id": null,
  "source_run_id": null,
  "source_diagnosis_id": null,
  "generated_at": null,
  "recommended_direction_id": null,
  "recommended_candidate_id": null,
  "candidates": [
    {
      "candidate_id": "cand_01",
      "direction_id": "dir_01",
      "rank_in_diagnosis": 1,
      "direction_name": null,
      "family_id": null,
      "family_guess_confidence": "low",
      "hypothesis": null,
      "expected_bottleneck": null,
      "code_locations": [],
      "risk": null,
      "metrics_to_recheck": [],
      "stop_condition": null,
      "fallback_score": null,
      "score_breakdown": {},
      "ranking_notes": [],
      "idea_origin": "auto-analysis"
    }
  ],
  "notes": "This file is derived from the diagnosis contract and should preserve exactly three candidates."
}
```

### `state/latest_attempt.json`

Current attempt bridge across selection, implementation, and measurement.

Primary use:

- records the single active attempt selected for `node_c`
- tracks build result before `node_a`
- records the measurement transition after `node_a`
- provides one place to classify the attempt outcome

Schema draft:

```json
{
  "schema_version": 1,
  "attempt_id": null,
  "status": "idle",
  "candidate_id": null,
  "direction_id": null,
  "direction_name": null,
  "family_id": null,
  "selection_mode": null,
  "selected_from_frontier_id": null,
  "selected_at": null,
  "source_run_id": null,
  "source_diagnosis_id": null,
  "selection_score": null,
  "score_breakdown": {},
  "ranking_notes": [],
  "implementation": {
    "commit": null,
    "build_status": null,
    "build_log_path": null,
    "touched_files": []
  },
  "measurement": {
    "run_id": null,
    "measurement_commit": null,
    "runtime_ms": null,
    "runtime_delta_ms": null,
    "tflops": null,
    "correctness": null,
    "headline_metrics": {},
    "headline_metric_deltas_vs_previous_run": {}
  },
  "transition_class": null,
  "close_reason": null,
  "notes": "Phase 2 turns the active implementation attempt into a first-class search record."
}
```

## Heuristic V1 Fallback Score

Phase 1 should use a simple, auditable fallback score instead of a deep or
opaque scorer.

The score should be numeric, but every component must also be surfaced in
`score_breakdown` and `ranking_notes`.

Suggested draft:

```text
fallback_score =
  rank_bonus
  + recommendation_bonus
  + family_prior
  + bottleneck_alignment
  + novelty_bonus
  - risk_penalty
  - recent_regression_penalty
  - duplicate_attempt_penalty
```

Suggested coarse terms:

- `rank_bonus`
  - `dir_01 = +3.0`
  - `dir_02 = +2.0`
  - `dir_03 = +1.0`
- `recommendation_bonus`
  - recommended direction: `+1.0`
  - otherwise: `0.0`
- `family_prior`
  - from `family_ledger.json`
  - coarse range: `[-2.0, +2.0]`
- `bottleneck_alignment`
  - if the candidate directly targets the latest measured dominant bottleneck:
    `+1.0`
  - otherwise: `0.0`
- `novelty_bonus`
  - new family or not recently tried: `+0.5`
  - otherwise: `0.0`
- `risk_penalty`
  - low: `0.0`
  - medium: `1.0`
  - high: `2.0`
- `recent_regression_penalty`
  - repeated recent regression in same family: `0.0` to `2.0`
- `duplicate_attempt_penalty`
  - near-duplicate of a just-failed candidate: `0.0` to `1.5`

The important rule is not the exact coefficients.

The important rule is:

- keep the numeric score coarse
- keep the explanation fields first-class
- allow future LLM reranking to override ties or near-ties using
  `ranking_notes`, not hidden precision

## Phase Acceptance Checks

### Phase 1 Acceptance Checks

- default files can be created with stable placeholder values and no behavior
  regressions
- `node_b` still writes exactly 3 directions in `state/latest_diagnosis.json`
- the 3 directions can be projected into `state/search_candidates.json`
  without losing `hypothesis`, `expected_bottleneck`, `code_locations`, `risk`,
  or `metrics_to_recheck`
- `state/search_frontier.json` can represent one open frontier and one selected
  candidate
- frontier selection still results in exactly one direction being handed to
  `node_c`
- if frontier metadata is missing, the workflow can still fall back to the
  current recommended-direction path

### Phase 2 Acceptance Checks

- `state/latest_attempt.json` exists and tracks the single active attempt across
  selection, build, and measurement
- `node_c` finalize can update build status in `latest_attempt` without making a
  performance claim
- `node_a` can classify the measured transition with a coarse outcome such as
  `improved`, `regressed`, `flat`, `build_failed`, or `restored_base`
- `state/search_closed.jsonl` receives one append-only close record per finished
  attempt or restore-base transition
- `state/family_ledger.json` updates aggregate family counts and coarse priors
  after measured outcomes
- restore-base remains explicit, auditable, and anchored to an accepted measured
  commit

### Phase 3 Acceptance Checks

- `heuristic_dataset/diagnoses.jsonl` can export candidate-level search fields
  such as `candidate_id`, `family_id`, `fallback_score`, `score_breakdown`, and
  `ranking_notes`
- `heuristic_dataset/attempts.jsonl` can export attempt-level search fields such
  as `attempt_id`, `selected_from_frontier_id`, `transition_class`, and
  `close_reason`
- export remains compatible with existing history when newer search fields are
  absent
- stronger scoring can incorporate family history and transition history, but
  still degrades cleanly to heuristic v1 fallback when evidence is missing
- selection remains explainable in plain JSON without requiring access to a
  remote model

## Non-Goals

- turning the repo into a general autotuning platform
- changing the fixed benchmark shape, dataset definition, or CUTLASS baseline
  semantics
- replacing the current script-first workflow with an always-on planner service
- letting `node_b` emit more than 3 directions
- letting `node_c` implement multiple directions in one loop
- claiming performance anywhere outside `node_a`
- introducing hidden, overfit, or fake-precision scoring without explanatory
  fields
- implementing full A*, MCTS, or arbitrary graph search in one refactor pass

## Suggested Implementation Order After This Spec

1. Add state defaults and rendering support for `search_state.json`,
   `search_frontier.json`, and `search_candidates.json`.
2. Project the finalized `node_b` diagnosis into normalized search candidates.
3. Add a minimal frontier selector that still falls back to the existing
   recommended-direction behavior.
4. Add `latest_attempt.json` and let `node_c` / `node_a` update it.
5. Append close records and family-ledger updates after measurement.
6. Extend `heuristic_dataset` export after the live state has stabilized.

This sequence keeps the first code changes additive and reversible.
