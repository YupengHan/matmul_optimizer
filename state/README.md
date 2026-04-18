# State directory

These files are the human-readable state layer of the repository.

## Purpose

The state layer is meant to be readable by:

- you,
- future AI agents,
- reviewers,
- and hiring managers who want to understand the optimization process.

## Files

## `progress.md`

Narrative progress log.

Use it to record:

- the current best result,
- the latest hypothesis,
- why a change was attempted,
- what happened after measurement.

## `current_focus.md`

One small, current snapshot:

- current branch,
- current bottleneck belief,
- active optimization direction,
- immediate next action.

## `human_review.md`

Queue for explicit human decisions.

Use it for:

- whether to keep a candidate,
- whether to widen scope,
- whether to allow a branch rewrite,
- whether to accept a tolerance policy change.

## `benchmark_baselines.md`

Single source of truth for:

- current CUTLASS baseline,
- current best custom kernel,
- gap to baseline.

## Update rules

### After every measured kernel attempt

Update:

- `progress.md`
- `current_focus.md`

### After every new best result

Update:

- `benchmark_baselines.md`
- optionally tag the commit

### After a diagnosis node proposes directions

Update:

- `human_review.md`

## What should not go here

Do not dump raw logs or giant metric tables in this directory.  
Raw machine artifacts belong under `runs/`.
