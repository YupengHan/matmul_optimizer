# Commit convention

Git is the auditable memory for this workflow.

The repo now uses node-specific commit prefixes:

- `node_a:` measured run state after a real evaluation
- `node_b:` diagnosis state with exactly three directions
- `node_c:` implementation commit after the build passes
- `infra:` repo-level workflow or protocol changes outside a single node loop

These prefixes are workflow roles, not generic code-style tags.

## Rules

### node_a

- commit only lightweight state
- never commit raw `runs/` artifacts
- only claim performance that came from the real harness
- when a round loop is active, include:
  - round label
  - implementation idea
  - runtime delta
  - TFLOP/s delta
  - profile paths

### node_b

- commit only lightweight state
- record the diagnosed source run
- record the recommended direction
- keep the three direction names searchable

### node_c

- commit code plus lightweight state
- do not create a success commit unless the build passed
- do not claim performance here; node_a must re-measure first

## Message template

`.gitmessage` mirrors this structure:

```text
node_x: <headline>

Why:
- workflow reason for this node
- why this step is happening now

What changed:
- code or state surface that changed
- direction or run being recorded

Measurement:
- node_a: runtime / TFLOP/s / correctness / key NCU metric
- node_b: source run id / source runtime / recommended direction
- node_c: build PASS and note that performance is pending node_a

Risk / follow-up:
- what the next node must do
```

## Good examples

```text
node_a: record run 20260418_111959_bf16_gemm_v1_host_v0 for bf16_gemm_v1_host_v0
```

```text
node_b: rank 3 directions from 20260418_111959_bf16_gemm_v1_host_v0
```

```text
node_c: implement dir_01 tensor-core multistage rewrite
```

## Bad examples

Avoid:

- `update kernel`
- `try idea`
- `fix stuff`
- `faster?`

Those lose the graph context and destroy auditability.
