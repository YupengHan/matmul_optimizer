# Supervisor protocol

This document defines the extra orchestration layer above `node_a -> node_b -> node_c -> node_a`.

It is intentionally small:

- the repo keeps execution script-first
- the main Codex agent acts as the supervisor
- `node_b` and `node_c` may use Codex `sub-agent`s
- repo-local Python does **not** attempt to spawn Codex agents

## Sources of truth

Read these first:

1. `state/supervisor_task.json`
2. `state/supervisor_context.md`
3. `state/graph_state.json`
4. the node-specific protocol for the current dispatch node

`state/supervisor_task.json` is the machine-readable dispatch contract. `state/supervisor_context.md` is the matching human-readable summary.

## Supervisor responsibilities

The main Codex agent owns:

- graph-aware dispatch
- loop continuation and stop conditions
- deciding whether the next step is direct script execution or a `sub-agent`
- running node finalize commands after a `sub-agent` returns
- verifying the workflow moves to the next graph node
- not prematurely terminating an active round loop just because a node finished and the next node is ready

The main Codex agent does **not**:

- claim performance without `node_a`
- skip build validation for `node_c`
- bypass the machine-readable state
- let a `sub-agent` mutate the loop policy

## Dispatch rule

If `state/supervisor_task.json` says:

- `dispatch_mode = direct_script`
  - run `prepare_command` directly from the main agent
  - this is the expected mode for `node_a`
- `dispatch_mode = sub_agent`
  - run `prepare_command` from the main agent if the node context is not fresh yet
  - spawn exactly one `sub-agent` for that node
  - give the sub-agent only the node-specific protocol and context
  - after the sub-agent returns, run `finalize_command` from the main agent

After every node completion, re-read `state/supervisor_task.json` before dispatching the next node.

## No-stop rule during active loops

If `state/round_loop_state.json` reports:

- `active = true`, and
- `remaining_rounds > 0`

then the supervisor must treat the workflow as still in-flight.

Operational consequences:

- `ready_for_node_b`, `ready_for_node_c`, and `ready_for_node_a` are continue states, not summary points
- a completed `node_a` that hands control back to `node_b` does not end the run
- the supervisor may emit progress updates, but must keep dispatching the next node
- the supervisor must not stop only because:
  - one round finished
  - a new node became ready
  - there is a useful intermediate performance summary to report

The supervisor may stop only when:

- `remaining_rounds = 0`
- the graph enters a failure / paused state
- a required permission or environment dependency blocks further execution

## Context-compression checkpoint rule

During an active multi-round loop, the supervisor must run a context-compression
checkpoint after every 5 completed rounds.

Operational consequences:

- refresh `state/supervisor_context.md` before dispatching past that checkpoint
- include the latest dispatch node, active round, remaining rounds, accepted base,
  and active direction or candidate in that checkpoint summary
- treat the checkpoint as a continue state, not a natural summary or stop point
- after refreshing the checkpoint, re-read `state/supervisor_task.json` and keep
  dispatching unless a real stop condition is present

## Node-specific sub-agent use

### `node_a`

- no `sub-agent`
- main agent runs `python scripts/graph.py node_a`
- must run outside the Codex sandbox with direct CUDA and Nsight Compute access
- after a real measurement finishes, node_a is also responsible for feeding the
  measured transition back into search memory (`search_state`, `family_ledger`,
  and `search_closed.jsonl` when a pending implementation attempt was actually measured)

### `node_b`

- main agent runs `python scripts/graph.py node_b`
- main agent spawns one diagnosis `sub-agent`
- the `sub-agent` follows `docs/node_b_protocol.md`
- after the `sub-agent` returns, the main agent runs `python scripts/graph.py node_b --finalize`

### `node_c`

- if no direction is selected, the main agent selects one first
- the preferred search-aware path is `python scripts/graph.py select-next`
- the legacy fallback path remains `python scripts/graph.py use-recommended-direction`
- main agent runs `python scripts/graph.py node_c`
- main agent spawns one implementation `sub-agent`
- the `sub-agent` follows `docs/node_c_protocol.md`
- after the `sub-agent` returns, the main agent runs `python scripts/graph.py node_c --finalize`

## Multi-round loop rule

To arm a planned loop:

```bash
python scripts/graph.py rounds --count N --auto-use-recommended
python scripts/graph.py rounds --count N --auto-select-frontier
```

Here `N` is the user-requested positive integer round budget.

Selection preference during an active loop:

- if `--auto-select-frontier` is active and node_c is entered with no selected direction, the supervisor should try `python scripts/graph.py select-next` first
  - `select-next` now chooses the best active family representative from the persistent frontier, which may be a reopened historical candidate rather than one of the latest 3 diagnosis directions
- if the frontier has no selectable open candidate, the supervisor may fall back to `python scripts/graph.py use-recommended-direction`
- if `--auto-select-frontier` is not active but `--auto-use-recommended` is active, the supervisor uses the legacy recommended-direction auto-select path

Then the supervisor repeats this control flow:

1. read `state/supervisor_task.json`
2. dispatch the current node
3. if the node used a `sub-agent`, run the finalize command after the `sub-agent` returns
4. re-read `state/supervisor_task.json`
5. stop only when:
   - `state/round_loop_state.json` reports `remaining_rounds = 0`, or
   - the graph enters a failure state that pauses the loop
6. otherwise continue immediately into the next dispatch step instead of treating the round boundary as a natural stopping point
7. after every 5 completed rounds, refresh `state/supervisor_context.md` as the required context-compression checkpoint and then continue immediately

One completed round is always:

```text
node_b -> node_c -> node_a
```

The round-level measurement record is the `node_a:` commit after the real re-measurement step.

That same `node_a` step is also the only place allowed to convert a build-passed
implementation attempt into a real search transition label such as `PASS_WIN`,
`PASS_FLAT`, or `PASS_LOSS`.

## Exploration branch rule

Default safety policy:

- if an experimental round regresses and there is no positive signal worth pursuing, the supervisor may restore the implementation surface from the current accepted measured commit before the next `node_b`

Use:

```bash
python scripts/graph.py restore-base --run-id <measured_run_id>
python scripts/graph.py restore-implementation --source-commit <measured_commit_sha>
```

`restore-base` is the first-class search-aware action. It resolves the run id to a
measured/source commit, restores only the implementation surface
(`src/kernels/*`, `src/runner/main.cpp`, `include/*`, `CMakeLists.txt`), and
records the restore in `search_state` / `latest_attempt` as a `family_id=restore_base`
action with `selection_mode=restore`.

`restore-implementation` remains the lower-level commit-addressed fallback when the
supervisor already knows the exact source commit to restore.

High-ceiling exploration policy:

- if a direction family shows partial signal or is judged necessary for a large target gap, the supervisor may intentionally keep exploring that family across multiple rounds even before it beats the current accepted base
- in that case, `node_b` should explicitly say whether the next round should continue the current exploration branch or return to the accepted base
- the accepted measured commit in `state/round_loop_state.json` still remains the comparison anchor until a later `node_a` run genuinely beats it
- use restoration selectively, not mechanically after every regressed round

## Audit rule

Use git commits as the durable audit log:

- `node_a:` measured result and delta
- `node_b:` diagnosis and ranked directions
- `node_c:` code implementation after build success

Do not treat a `sub-agent` response as completed work until the main agent has run the node finalize command and confirmed the graph state moved forward.
