# Search Policy

This document records the current planning and search policy for the
heuristic-search workflow in `scripts/graph.py`.

It is intentionally maintained as an internal engineering note rather than a
main entry document. The goal is to preserve enough rationale and policy detail
that future maintainers can safely adjust planning behavior without reverse
engineering the code path from scratch.

## Purpose

The workflow now supports a persistent historical frontier, but it does **not**
score every historical candidate on every step.

Instead, the planner uses a **family-representative frontier**:

- all historical candidates remain recorded in the persistent frontier
- each family exposes at most one active representative candidate at a time
- historical candidates may re-enter the active pool through explicit reopen
  rules
- `select-next` competes only across active family representatives

This keeps search complexity bounded while still allowing long-ago but
potentially useful directions to come back automatically.

## Design Goals

- Preserve the existing `node_b -> node_c -> node_a` loop.
- Keep `node_b` responsible for generating exactly 3 new directions.
- Allow historical candidates to re-enter the candidate pool automatically.
- Avoid a naive "score every past state every round" implementation.
- Reorder candidates **inside** each family when new evidence arrives.
- Make the policy observable from repo-local state and docs.

## Non-Goals

- This is not a full A* implementation.
- This does not maintain an arbitrary graph search over every code state.
- This does not branch into multiple concurrent `node_c` implementations.
- This does not try to auto-edit or auto-rewrite `node_b` diagnosis text.

## State Model

Primary machine-readable state:

- `state/search_frontier.json`
  Persistent candidate history plus the currently active family
  representatives.
- `state/search_candidates.json`
  The latest normalized 3-candidate projection from the most recent `node_b`
  diagnosis.
- `state/search_closed.jsonl`
  Append-only close log for measured and build-failure outcomes.
- `state/family_ledger.json`
  Family-level aggregate memory.
- `state/latest_attempt.json`
  The active implementation/measurement bridge.
- `state/search_state.json`
  Global search pointers and policy defaults.

## Core Policy

### 1. Persistent Frontier

`node_b --finalize` no longer overwrites the frontier with only the latest 3
directions.

Instead it:

1. normalizes the latest 3 diagnosis directions into candidate records
2. merges them into the persistent frontier history
3. refreshes family representatives
4. leaves `search_candidates.json` as the latest 3-direction snapshot

The frontier therefore acts as a durable candidate memory, while
`search_candidates.json` remains a latest-diagnosis projection.

### 2. Family Representatives

The active search pool is bounded by family.

At any point:

- a family may have many historical candidates in the persistent frontier
- only one candidate in that family should be the current representative
- the representative is the only candidate from that family that remains
  `open` or `reopened`
- sibling candidates in the same family are parked when they are not the
  representative

This is the main complexity-control rule.

### 3. Family-Internal Reorder

Families are re-ordered by event, not by a background full-rescore loop.

Current reorder triggers:

1. `node_b --finalize`
   New candidate metadata enters the frontier and can reorder the family.
2. `node_c --finalize` build failure
   The selected candidate is closed as `BUILD_FAIL`, family memory updates, and
   the family is re-ranked.
3. `node_a`
   The selected candidate is closed with measured outcome
   (`PASS_WIN` / `PASS_FLAT` / `PASS_LOSS` / `CORRECTNESS_FAIL`), family memory
   updates, and the family is re-ranked.

This means family ordering changes only when the repo has new evidence.

### 4. Representative Score

Within a family, candidate ordering currently uses a heuristic effective score
derived from:

- candidate priority / `search_score_v1`
- freshness bonus from the source search iteration
- recommended-direction bonus
- predicted fail-risk penalty
- measured outcome penalty
- reopen-count penalty
- family-level loss / fail penalties

This is still heuristic and intentionally auditable. It is meant to be easy to
change as we accumulate more search history.

### 5. Reopen Rules

Historical candidates can re-enter the pool only through bounded reopen rules.

Current default policy:

- reopen only candidates that previously closed as:
  - `PASS_FLAT`
  - `PASS_LOSS`
  - `DIAG_POS_RUNTIME_NEG`
- do **not** reopen:
  - `BUILD_FAIL`
  - `CORRECTNESS_FAIL`
- reopen at most once per candidate by default
- require at least one later search iteration after the close event
- reject reopen if the family has recorded any build/correctness fail
- reject reopen if the family has accumulated too many losses
- for loss-based reopen, the historical loss must still be bounded:
  - `abs(last_runtime_delta_ms) <= max(reopen_loss_tolerance_ms, predicted_gain_ms)`
- require predicted fail risk to remain below the configured ceiling

Current defaults live in `search_state.selection_policy`:

- `policy_id = family_representative_v2`
- `max_reopens_per_candidate = 1`
- `reopen_loss_tolerance_ms = 0.15`
- `reopen_fail_risk_ceiling = 0.6`

### 6. Selection

`select-next` is now candidate-centric.

It no longer assumes the selected item must be one of the directions present in
the current `latest_diagnosis.json`.

The flow is:

1. normalize and reconcile the persistent frontier
2. refresh family representatives
3. inspect only `open` / `reopened` representative candidates
4. choose the best representative across families
5. materialize `state/active_direction.json` from the candidate summary itself

This is what allows an older candidate to be selected even if it is not present
in the latest diagnosis payload.

### 7. Node C Context

`node_c` can now proceed from candidate-native summary metadata.

That matters because a reopened historical candidate may come from an older
diagnosis file, not the latest one. The active candidate must therefore carry a
self-contained summary of:

- hypothesis
- expected bottleneck
- code locations
- risk
- metrics to recheck

## Maintenance Guidance

When modifying this policy, update both the code and this file.

Recommended checklist:

1. If you change reopen eligibility, update the thresholds and rationale here.
2. If you change family scoring, document the new inputs and penalties.
3. If you add new frontier statuses, document their lifecycle meaning here.
4. If you change the active representative rule, update the complexity-control
   section first.
5. If you add richer historical priors, note whether they affect:
   - merge
   - reorder
   - reopen
   - selection

## Likely Future Extensions

- richer family priors from accumulated branch-local history
- explicit family-level cooldowns
- separate reopen budgets for exploit vs explore families
- global top-k family cap beyond the current one-representative-per-family rule
- learned score adjustments using accumulated close history
- explicit restore-base candidate generation integrated into family competition

## Code Touchpoints

Current implementation centers on:

- `scripts/graph.py`
  - frontier normalization and reconciliation
  - family representative refresh
  - candidate selection
  - node_a / node_c writeback into search memory
- `scripts/state_lib.py`
  - default policy and frontier schema defaults

If this file drifts from the implementation, treat the code as authoritative and
update this document in the same commit that changes policy behavior.
