# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_a`
- dispatch mode: `direct_script`
- graph status: `ready_for_node_a`
- round label: `round 1/100`
- round loop active: `yes`
- rounds remaining: `100`
- auto-select frontier: `no`
- latest run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- latest runtime: `24.186960 ms`
- recommended direction: `dir_01`
- active direction: `dir_01`
- display update due at current checkpoint: `no`
- watchdog status: `healthy`
- continue required now: `yes`
- stop allowed now: `no`
- natural stop states disallowed: `yes`
- interrupt policy: `only_explicit_user_redirect`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `AGENTS.md`
- prepare command: `python scripts/graph.py node_a`
- current dispatch requires direct GPU access: `yes`

## Dispatch rule

- run the script-first node directly from the main agent
- do not spawn a sub-agent for node_a
- after node_a finishes, re-read `state/supervisor_task.json` and continue

## Multi-round loop

- active loop: `round 1/100` with `100` rounds remaining
- auto-use recommended: `yes`
- auto-select frontier: `no`
- context compression cadence: every `5` completed rounds
- public display refresh cadence: every `5` completed rounds
- next context compression checkpoint: after `5` completed rounds
- next display refresh checkpoint: after `5` completed rounds
- display refresh checkpoint open now: `no`
- display refresh action: Use the matmul-doc-sync skill or an equivalent narrow doc-refresh pass to update `README.md`, `blog/harness-engineering-human-in-the-loop-cuda-matmul/index.md`, and the rendered optimization tree, then commit only those doc/image files and run `git push origin master`.
- continue until: `remaining_rounds == 0 or explicit_user_redirect`
- immediate continue instruction: Continue now by running `python scripts/graph.py node_a` outside the sandbox, then re-read `state/supervisor_task.json`.
- allowed stop reasons while loop is active: `round_loop_complete, graph_failure_or_pause, permission_or_environment_block, explicit_user_redirect`
- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop

## Watchdog

- timeout: `10` minutes without workflow changes
- latest observed progress: `2026-04-21T11:09:29-07:00` via `state/graph_state.json`
- idle minutes: `0.0`
- watchdog status: `healthy`
- continue instruction: `No watchdog action is currently required.`

## Notes

- `Run node_a directly from the main Codex agent outside the sandbox, then re-read graph state. Active round loop in progress: `ready_for_node_a` is a continue state, not a legal stop point. Re-read `state/supervisor_task.json` after every node and keep dispatching until `remaining_rounds = 0`, the graph fails/pauses, a required permission or environment dependency blocks execution, or the user explicitly redirects the conversation.`
