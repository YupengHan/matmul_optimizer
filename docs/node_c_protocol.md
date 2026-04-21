# Node C protocol

Node C is the implementation node. It consumes one selected direction, makes one bounded code change, proves the code still builds, commits that implementation, then hands control back to node_a.

In the intended workflow, Node C is executed by one implementation `sub-agent` under the main Codex supervisor.

## Entry

Select a direction first:

```bash
python scripts/graph.py select-next
```

or:

```bash
python scripts/graph.py approve --direction dir_02
```

or:

```bash
python scripts/graph.py use-recommended-direction
```

Prepare the implementation context:

```bash
python scripts/graph.py node_c
```

Finalize after editing code:

```bash
python scripts/graph.py node_c --finalize
```

The main Codex supervisor is responsible for the prepare and finalize commands. The `sub-agent` owns the bounded code edit.

## Required inputs

Read:

1. `state/node_c_context.md`
2. `state/active_direction.json`
3. `state/latest_diagnosis.json`
4. `state/current_focus.md`
5. the code files named in the selected direction's `code_locations`

Note:

- the selected candidate may come from the persistent frontier rather than the latest 3 directions
- when that happens, `state/active_direction.json` is the authoritative summary for implementation details

The supervisor should also read:

- `docs/supervisor_protocol.md`
- `state/supervisor_task.json`

## Allowed modification surface

Default allowed files:

- `src/kernels/*`
- `src/runner/main.cpp`
- `include/*`
- `CMakeLists.txt` only when genuinely required
- lightweight state files under `state/`

Do not widen scope unless the selected direction truly requires minimal runner or interface glue.

## Execution rule

Implement exactly one direction. Do not combine extra optimizations in the same node_c loop.

Treat the selected direction as the primary family for this loop. If the implementation
has to cross into another idea family, record that explicitly in
`state/active_direction.json` via `secondary_family_ids` instead of silently widening scope.

## Sub-agent boundary

The implementation `sub-agent` should:

- read the selected direction and its code locations
- edit only the files required for that one direction
- keep the implementation aligned with the planned action fingerprint when possible
- if the implementation drifts semantically, update `implemented_action_fingerprint`,
  `semantic_delta_tags`, and `actual_code_regions` in `state/active_direction.json`
- if the edit crosses families, write `secondary_family_ids` before finalize
- leave build validation and finalize orchestration to the main agent

After the `sub-agent` returns, the main Codex supervisor must run:

```bash
python scripts/graph.py node_c --finalize
```

## Build rule

`python scripts/graph.py node_c --finalize` is the build gate.

It must:

- configure the repo for the main loop without requiring CUTLASS
- build `custom_runner`
- stop immediately if the build fails
- write `state/latest_attempt.json` even when the build fails, with `build_status=FAIL`
  and a structured `failure_mode`
- update failure state if the build fails
- avoid writing a success commit on build failure

## Success path

On success, finalize will:

- mark the selected direction as implemented
- write `state/latest_attempt.json` with the explicit implementation edge from selected
  candidate to built code change
- commit code plus lightweight state
- auto-run node_a by default
- if a round loop is active, keep the round open until node_a measures the result

That means the normal loop is:

```text
node_c --finalize -> node_a -> node_b
```

## Performance-claim rule

Node C never claims a speedup. Only node_a may record performance conclusions, because only node_a runs the real measurement harness.

## Commit rule

Node C commit message must explain:

- which direction id was implemented
- why that direction was chosen
- which files changed
- that the build passed
- that performance is still pending node_a re-measurement
