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

## Node-specific sub-agent use

### `node_a`

- no `sub-agent`
- main agent runs `python scripts/graph.py node_a`
- must run outside the Codex sandbox with direct CUDA and Nsight Compute access

### `node_b`

- main agent runs `python scripts/graph.py node_b`
- main agent spawns one diagnosis `sub-agent`
- the `sub-agent` follows `docs/node_b_protocol.md`
- after the `sub-agent` returns, the main agent runs `python scripts/graph.py node_b --finalize`

### `node_c`

- if no direction is selected, the main agent selects one first
- main agent runs `python scripts/graph.py node_c`
- main agent spawns one implementation `sub-agent`
- the `sub-agent` follows `docs/node_c_protocol.md`
- after the `sub-agent` returns, the main agent runs `python scripts/graph.py node_c --finalize`

## Multi-round loop rule

To arm a planned loop:

```bash
python scripts/graph.py rounds --count 5 --auto-use-recommended
```

Then the supervisor repeats this control flow:

1. read `state/supervisor_task.json`
2. dispatch the current node
3. if the node used a `sub-agent`, run the finalize command after the `sub-agent` returns
4. re-read `state/supervisor_task.json`
5. stop only when:
   - `state/round_loop_state.json` reports `remaining_rounds = 0`, or
   - the graph enters a failure state that pauses the loop

One completed round is always:

```text
node_b -> node_c -> node_a
```

The round-level measurement record is the `node_a:` commit after the real re-measurement step.

## Regression recovery rule

When a multi-round experiment wants to preserve every failed attempt in git history but avoid building the next round on top of a regressed implementation:

1. let `node_a` finish and record the regressed run normally,
2. keep the `node_c:` and `node_a:` commits in history,
3. restore the node_c-owned code surface from the previous accepted measured commit before the next `node_b`.

Use:

```bash
python scripts/graph.py restore-implementation --source-commit <measured_commit_sha>
```

This command restores only the implementation surface (`src/kernels/*`, `src/runner/main.cpp`, `include/*`, `CMakeLists.txt`) and leaves the recorded lightweight state and run history intact.

Applied policy for monotonic experiments:

- if round `i` is worse than round `i-1`, keep round `i` recorded,
- then start round `i+1` from the code of round `i-1`,
- do not stack round `i+1` on top of the regressed code from round `i`.

## Audit rule

Use git commits as the durable audit log:

- `node_a:` measured result and delta
- `node_b:` diagnosis and ranked directions
- `node_c:` code implementation after build success

Do not treat a `sub-agent` response as completed work until the main agent has run the node finalize command and confirmed the graph state moved forward.
