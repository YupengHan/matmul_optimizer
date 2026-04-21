# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_c`
- dispatch mode: `sub_agent`
- graph status: `ready_for_node_c`
- round label: `round 32/100`
- round loop active: `yes`
- rounds remaining: `69`
- auto-select frontier: `no`
- latest run id: `20260421_013804_bf16_gemm_v1_b8a113b`
- latest runtime: `24.168880 ms`
- recommended direction: `dir_01`
- active direction: `dir_01`
- display update due at current checkpoint: `no`
- watchdog status: `healthy`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_c_protocol.md`
- node context file: `state/node_c_context.md`
- prepare command: `python scripts/graph.py node_c`
- finalize command: `python scripts/graph.py node_c --finalize`
- current dispatch requires direct GPU access: `no`

## Dispatch rule

- main agent stays responsible for graph state, commits, and loop control
- spawn exactly one sub-agent for the current node
- after the sub-agent returns, run the finalize command from the main agent
- then re-read `state/supervisor_task.json` before dispatching the next node

## Multi-round loop

- active loop: `round 32/100` with `69` rounds remaining
- auto-use recommended: `yes`
- auto-select frontier: `no`
- context compression cadence: every `5` completed rounds
- public display refresh cadence: every `5` completed rounds
- last context compression checkpoint: after `30` completed rounds
- next context compression checkpoint: after `35` completed rounds
- last display refresh checkpoint: after `30` completed rounds
- next display refresh checkpoint: after `35` completed rounds
- display refresh checkpoint open now: `no`
- display refresh action: Use the matmul-doc-sync skill or an equivalent narrow doc-refresh pass to update `README.md`, `blog/harness-engineering-human-in-the-loop-cuda-matmul/index.md`, and the rendered optimization tree, then commit only those doc/image files.
- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop

## Watchdog

- timeout: `10` minutes without workflow changes
- latest observed progress: `2026-04-21T01:40:10-07:00` via `state/graph_state.json`
- idle minutes: `0.0`
- watchdog status: `healthy`
- continue instruction: `No watchdog action is currently required.`

## Notes

- `Ensure exactly one direction is selected, spawn an implementation sub-agent, then finalize node_c from the main Codex agent.`
