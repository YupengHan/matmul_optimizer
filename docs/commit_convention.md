# Commit and branch convention

Git is the long-term memory system for this project.

A good performance commit must explain:

- what bottleneck was targeted,
- why the code changed,
- what the kernel idea was,
- what evidence motivated it,
- and what improvement was observed.

## Branch policy

## `main`

`main` should stay readable and meaningful.

Only merge to `main` when:

1. build passes,
2. correctness passes,
3. performance was re-measured,
4. the change is documented,
5. the claimed improvement is real.

## Feature branches

Use feature branches for:

- out-of-box experiments,
- aggressive rewrites,
- anything likely to regress,
- branch-only hypothesis testing.

Suggested pattern:

- `feat/tile-retune`
- `feat/cpasync-staging`
- `feat/swizzle-layout`
- `exp/outbox-hypothesis-01`

## Commit message format

Suggested prefix set:

- `perf:` measured performance improvement
- `fix:` correctness or build fix
- `refactor:` structural cleanup with no intended perf claim
- `infra:` scripts, docs, pipeline, or benchmark harness updates
- `baseline:` CUTLASS or reference baseline updates
- `wip:` temporary local work; avoid merging these

## Strongly recommended format for perf commits

```text
perf: +X.XX% on fixed_bf16_gemm_v1 by <short idea>

Why:
- what bottleneck was targeted
- what evidence supported that belief

What changed:
- code-level description
- tile / pipeline / layout / launch changes

Measurement:
- previous median runtime: ...
- new median runtime: ...
- delta: ...
- TFLOP/s delta: ...
- correctness: PASS / FAIL
- NCU headline changes: ...

Risk / follow-up:
- what may still be fragile
- what should be tested next
```

## Tagging best results

When a new best kernel is confirmed, tag it.

Suggested tags:

- `best-v0`
- `best-v1`
- `best-v2`

Also update `state/benchmark_baselines.md`.

## Minimum required evidence for a performance claim

A measured improvement should include:

- benchmark case ID,
- runtime statistic used,
- number of warmups,
- number of timed iterations,
- correctness status,
- date,
- branch or commit hash,
- whether NCU was run.

## Bad commit examples

Avoid commits like:

- `update kernel`
- `try something`
- `fix`
- `faster?`

These destroy the memory value of git.

## Good commit examples

### Example 1

```text
perf: +4.8% on fixed_bf16_gemm_v1 by shrinking CTA tile

Why:
- tensor utilization was low and register-limited occupancy looked weak

What changed:
- reduced CTA tile from ...
- reduced accumulator footprint
- adjusted launch configuration

Measurement:
- previous median runtime: ...
- new median runtime: ...
- TFLOP/s delta: ...
- correctness: PASS
- NCU headline changes: more active warps, lower stall_long_scoreboard

Risk / follow-up:
- shared reuse may have weakened
- compare against a deeper copy pipeline next
```

### Example 2

```text
baseline: refresh CUTLASS profile for fixed_bf16_gemm_v1

Why:
- 10 non-improving rounds since last baseline refresh

What changed:
- reran CUTLASS timing
- collected new NCU rep and summary
- updated state baseline file
```
