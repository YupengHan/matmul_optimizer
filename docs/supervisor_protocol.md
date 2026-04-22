# Supervisor protocol

This document defines the extra orchestration layer above `node_a -> node_b -> node_c -> node_a`.

It is intentionally small:

- the repo keeps execution script-first
- the main LLM agent acts as the supervisor
- `node_b` and `node_c` may use LLM `sub-agent`s
- repo-local Python does **not** attempt to spawn LLM agents

## Sources of truth

Read these first:

1. `state/supervisor_task.json`
2. `state/supervisor_context.md`
3. `state/graph_state.json`
4. the node-specific protocol for the current dispatch node

`state/supervisor_task.json` is the machine-readable dispatch contract. `state/supervisor_context.md` is the matching human-readable summary.

## Supervisor responsibilities

The main LLM agent owns:

- graph-aware dispatch
- loop continuation and stop conditions
- deciding whether the next step is direct script execution or a `sub-agent`
- running node finalize commands after a `sub-agent` returns
- verifying the workflow moves to the next graph node
- not prematurely terminating an active round loop just because a node finished and the next node is ready

The main LLM agent does **not**:

- claim performance without `node_a`
- skip build validation for `node_c`
- bypass the machine-readable state
- let a `sub-agent` mutate the loop policy
- replace `node_b` or `node_c` with a repo-external scripted helper that synthesizes diagnosis or implementation work

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
- the user explicitly redirects the conversation away from the active loop

## Machine-readable continue contract

When a multi-round loop is active, `state/supervisor_task.json` must also carry
an explicit stop contract, not only prose guidance.

Required meanings:

- `continue_required = true`
  - the current supervisor turn must keep dispatching; this is not a legal stop point
- `stop_allowed = false`
  - `ready_for_node_b`, `ready_for_node_c`, `ready_for_node_a`, and checkpoint states
    are continue states while the loop is active
- `continue_until = "remaining_rounds == 0 or explicit_user_redirect"`
  - the loop continues until the budget finishes, unless the user explicitly changes topics
- `continue_instruction`
  - the immediate next dispatch action for the current node
- `interrupt_policy = "only_explicit_user_redirect"`
  - an intermediate summary, a completed round, or a newly ready node is not enough to stop

Allowed stop reasons while `continue_required = true`:

- `round_loop_complete`
- `graph_failure_or_pause`
- `permission_or_environment_block`
- `explicit_user_redirect`

## Context-compression and display-refresh checkpoint rule

During an active multi-round loop, the supervisor must run a context-compression
checkpoint after every 5 completed rounds.

Operational consequences:

- refresh `state/supervisor_context.md` before dispatching past that checkpoint
- include the latest dispatch node, active round, remaining rounds, accepted base,
  active direction or candidate, display-refresh checkpoint state, and watchdog
  state in that checkpoint summary
- at that same 5-round checkpoint, refresh the public display content:
  - `README.md`
  - `blog/harness-engineering-human-in-the-loop-cuda-matmul/index.md`
  - `blog/harness-engineering-human-in-the-loop-cuda-matmul/matmul_optimization_tree_pretty.svg`
  - `blog/harness-engineering-human-in-the-loop-cuda-matmul/matmul_optimization_tree_pretty.png`
- use the `matmul-doc-sync` skill or an equivalent narrow doc-refresh pass
- commit only the doc/image files touched by that display refresh
- run `git push origin HEAD` after the checkpoint doc/image commit so the current branch state is published remotely
- treat the checkpoint as a continue state, not a natural summary or stop point
- after refreshing the checkpoint, re-read `state/supervisor_task.json` and keep
  dispatching unless a real stop condition is present

## Watchdog rule

During an active multi-round loop, the supervisor must also watch for idle stalls.

Operational consequences:

- if 10 minutes pass with no repo-visible workflow progress and `remaining_rounds > 0`,
  treat the loop as stalled rather than completed
- re-read `state/supervisor_task.json` and use the emitted continue instruction for
  the current dispatch node
- if the current dispatch is `node_b` or `node_c`, the continue instruction still
  preserves the normal supervisor contract:
  - prepare or refresh the node context if needed
  - spawn exactly one `sub-agent`
  - run the finalize command from the main agent
- the watchdog is a continue mechanism, not a stop condition on its own

## Node-specific sub-agent use

### `node_a`

- no `sub-agent`
- main agent runs `python scripts/graph.py node_a`
- must run outside the LLM sandbox with direct CUDA and Nsight Compute access
- after a real measurement finishes, node_a is also responsible for feeding the
  measured transition back into search memory (`search_state`, `family_ledger`,
  and `search_closed.jsonl` when a pending implementation attempt was actually measured)

### `node_b`

- main agent runs `python scripts/graph.py node_b`
- main agent spawns one diagnosis `sub-agent`
- the `sub-agent` follows `docs/node_b_protocol.md`
- the supervisor must not replace this reasoning step with a template emitter or repo-external helper
- after the `sub-agent` returns, the main agent runs `python scripts/graph.py node_b --finalize`

### `node_c`

- if no direction is selected, the main agent selects one first
- the preferred search-aware path is `python scripts/graph.py select-next`
- the legacy fallback path remains `python scripts/graph.py use-recommended-direction`
- main agent runs `python scripts/graph.py node_c`
- main agent spawns one implementation `sub-agent`
- the `sub-agent` follows `docs/node_c_protocol.md`
- the supervisor must require a real compiled-code edit and must not treat a scripted history replay loop as valid implementation work
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
7. after every 5 completed rounds, refresh `state/supervisor_context.md`, refresh the public display content, commit only the doc/image refresh, and then continue immediately
8. if the loop stays active and the 10-minute watchdog later fires, issue the current continue instruction instead of treating the idle gap as a natural stop

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
